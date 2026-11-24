"""Link Slack directly to the visible Actions job summary, not the run header."""
import json
import os
import re
import urllib.request


def summary_url():
    repo, run_id = os.getenv('GITHUB_REPOSITORY', ''), os.getenv('GITHUB_RUN_ID', '')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo) or not run_id.isdigit():
        return None
    base = f'https://github.com/{repo}/actions/runs/{run_id}'
    token = os.getenv('GH_ACTIONS_READ_TOKEN')
    if not token:
        return base
    try:
        attempt = os.getenv('GITHUB_RUN_ATTEMPT', '1')
        if not attempt.isdigit():
            return base
        request = urllib.request.Request(
            f'https://api.github.com/repos/{repo}/actions/runs/{run_id}/attempts/{attempt}/jobs',
            headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json'})
        with urllib.request.urlopen(request, timeout=10) as response:
            jobs = json.load(response)['jobs']
        matches = [j for j in jobs if j['name'] == os.getenv('GITHUB_JOB', 'audit')]
        if len(matches) == 1 and isinstance(matches[0].get('id'), int):
            return base + '#summary-' + str(matches[0]['id'])
    except Exception:
        # Never log a request/exception that could contain the token.
        print('::warning title=상세보기 연결::작업 위치 조회 실패: 실행 화면의 audit 요약에서 상세 보고서를 확인하세요.')
    return base
