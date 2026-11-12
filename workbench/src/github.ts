const API = 'https://api.github.com';
const OUTPUTS = ['logging.ts', 'KoinEvents.kt', 'catalog.md', 'manifest.json'] as const;

export class GithubError extends Error {
  readonly status: number;
  readonly recovery?: string;
  constructor(message: string, status = 502, recovery?: string) {
    super(message);
    this.status = status;
    this.recovery = recovery;
  }
}

type GithubFetch = typeof fetch;
type GitFile = { path: string; sha: string };

type GithubClient = {
  request<T>(path: string, method?: string, body?: unknown): Promise<T>;
};

function client(token: string, repository: string, fetcher: GithubFetch): GithubClient {
  if (!/^[\w.-]+\/[\w.-]+$/.test(repository)) throw new GithubError('GitHub 저장소 설정이 잘못되었습니다.', 503);
  return {
    async request<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
      let response: Response;
      try {
        response = await fetcher(`${API}/repos/${repository}${path ? `/${path}` : ''}`, {
          method,
          redirect: 'error',
          signal: AbortSignal.timeout(12000),
          headers: {
            Authorization: `Bearer ${token}`,
            Accept: 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'koin-logging-workbench',
            ...(body === undefined ? {} : { 'Content-Type': 'application/json' }),
          },
          ...(body === undefined ? {} : { body: JSON.stringify(body) }),
        });
      } catch {
        throw new GithubError('GitHub에 연결할 수 없습니다. 나중에 다시 시도하세요.', 503);
      }
      if (!response.ok) {
        if (response.status === 409 || response.status === 422) throw new GithubError('GitHub 변경 충돌입니다. 최신 스냅샷에서 다시 시작하세요.', 409);
        if (response.status === 401 || response.status === 403 || response.status === 404) throw new GithubError('GitHub 저장소 접근 권한 또는 토큰을 확인하세요.', 503);
        throw new GithubError('GitHub 요청에 실패했습니다. 나중에 다시 시도하세요.', 502);
      }
      try {
        return await response.json() as T;
      } catch {
        throw new GithubError('GitHub 응답 형식이 올바르지 않습니다.', 502);
      }
    },
  };
}

export async function remoteStatus(token: string, repository: string, fetcher: GithubFetch = fetch): Promise<{ branch: string; head: string }> {
  const api = client(token, repository, fetcher);
  const repositoryInfo = await api.request<{ full_name: string; default_branch: string }>('');
  if (repositoryInfo.full_name?.toLowerCase() !== repository.toLowerCase() || !/^[\w./-]+$/.test(repositoryInfo.default_branch)) {
    throw new GithubError('GitHub 저장소 응답이 요청한 저장소와 다릅니다.', 503);
  }
  const branch = repositoryInfo.default_branch;
  const ref = await api.request<{ object: { sha: string } }>(`git/ref/heads/${encodeURIComponent(branch)}`);
  if (!/^[a-f0-9]{40}$/.test(ref.object?.sha)) throw new GithubError('GitHub 기준 커밋이 올바르지 않습니다.', 502);
  return { branch, head: ref.object.sha };
}

export async function createProposal(input: {
  token: string;
  repository: string;
  snapshotCommit: string;
  expectedFiles: GitFile[];
  specPath: string;
  specText: string;
  title: string;
  generated: Record<string, string>;
}, fetcher: GithubFetch = fetch): Promise<{ url: string }> {
  const api = client(input.token, input.repository, fetcher);
  const current = await remoteStatus(input.token, input.repository, fetcher);
  if (current.head !== input.snapshotCommit) throw new GithubError('원격 기본 브랜치가 스냅샷 이후 변경되었습니다. 스냅샷을 새로 준비하세요.', 409);
  if (!input.expectedFiles.some(f => f.path === input.specPath)) {
    // A new spec is permitted only when it has no existing path at the base commit.
    const path = `contents/${input.specPath.split('/').map(encodeURIComponent).join('/')}?ref=${current.head}`;
    let response: Response;
    try {
      response = await fetcher(`${API}/repos/${input.repository}/${path}`, {
        redirect: 'error', signal: AbortSignal.timeout(12000),
        headers: { Authorization: `Bearer ${input.token}`, Accept: 'application/vnd.github+json', 'User-Agent': 'koin-logging-workbench' },
      });
    } catch {
      throw new GithubError('새 명세 경로를 확인할 수 없습니다.', 503);
    }
    if (response.status !== 404) throw new GithubError(response.ok ? '명세 파일이 원격에 이미 존재합니다.' : '새 명세 경로를 확인할 수 없습니다.', response.ok ? 409 : 503);
  }
  for (const file of input.expectedFiles) {
    const remote = await api.request<{ sha: string }>(`contents/${file.path.split('/').map(encodeURIComponent).join('/')}?ref=${current.head}`);
    if (remote.sha !== file.sha) throw new GithubError(`원격 원본이 스냅샷과 다릅니다: ${file.path}`, 409);
  }
  const commit = await api.request<{ tree: { sha: string } }>(`git/commits/${current.head}`);
  if (!/^[a-f0-9]{40}$/.test(commit.tree?.sha)) throw new GithubError('GitHub 트리 응답이 올바르지 않습니다.', 502);
  const tree = await api.request<{ sha: string }>('git/trees', 'POST', {
    base_tree: commit.tree.sha,
    tree: [
      { path: input.specPath, mode: '100644', type: 'blob', content: input.specText },
      ...OUTPUTS.map(name => ({ path: `generated/${name}`, mode: '100644', type: 'blob', content: input.generated[name] })),
    ],
  });
  if (!/^[a-f0-9]{40}$/.test(tree.sha)) throw new GithubError('GitHub 트리 생성에 실패했습니다.', 502);
  const result = await api.request<{ sha: string }>('git/commits', 'POST', {
    message: input.title,
    tree: tree.sha,
    parents: [current.head],
  });
  if (!/^[a-f0-9]{40}$/.test(result.sha)) throw new GithubError('GitHub 커밋 생성에 실패했습니다.', 502);
  const branch = `workbench/${new Date().toISOString().slice(0, 10)}-${crypto.randomUUID()}`;
  await api.request('git/refs', 'POST', { ref: `refs/heads/${branch}`, sha: result.sha });
  const recovery = `https://github.com/${input.repository}/compare/${encodeURIComponent(current.branch)}...${branch}`;
  try {
    const after = await remoteStatus(input.token, input.repository, fetcher);
    if (after.head !== current.head) throw new GithubError('원격 기본 브랜치가 변경되었습니다. 생성된 브랜치를 확인하세요.', 409);
    const pr = await api.request<{ html_url: string }>('pulls', 'POST', {
      title: input.title,
      head: branch,
      base: current.branch,
      body: 'Canonical logging workbench proposal. Generated outputs are calculated from the full validated canonical model. Review evidence and platform support before merging.',
    });
    const match = /^https:\/\/github\.com\/([^/]+\/[^/]+)\/pull\/[1-9]\d*$/.exec(pr.html_url || '');
    if (match?.[1].toLowerCase() !== input.repository.toLowerCase()) throw new GithubError('PR 응답이 올바르지 않습니다.', 502);
    return { url: pr.html_url };
  } catch (error) {
    throw new GithubError(error instanceof Error ? error.message : 'PR 생성에 실패했습니다.', error instanceof GithubError ? error.status : 502, recovery);
  }
}
