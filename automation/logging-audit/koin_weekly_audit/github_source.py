"""Read every tracked specification from the workflow's pinned main checkout."""
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

from .contracts import clean
from .notion_source import IncompleteSource


class GitHubSource:
    def __init__(self, root=None, revision=None, tracked_paths=None):
        self.root = Path(root or os.environ.get('GITHUB_WORKSPACE', Path(__file__).resolve().parents[3])).resolve()
        self.revision = revision or os.getenv('GITHUB_SHA', '')
        self.tracked_paths = tracked_paths

    def collect(self):
        if not re.fullmatch(r'[a-f0-9]{40}', self.revision):
            raise IncompleteSource('Pinned GitHub revision missing', code='github_revision_missing')
        paths = self.tracked_paths
        if paths is None:
            head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root, text=True).strip()
            if head != self.revision:
                raise IncompleteSource('Checkout revision mismatch', code='github_revision_mismatch')
            paths = subprocess.check_output(['git', 'ls-files', '-z', '--', 'event-log/'], cwd=self.root).decode('utf8').split('\0')
        files = sorted(p for p in paths if p.endswith('.md') and Path(p).name != 'README.md')
        services = {p.split('/')[1] for p in files}
        if len(files) < 700 or len(services) < 21:
            raise IncompleteSource('GitHub specification scope reduced', code='github_scope_reduced')
        pages, counts = [], {}
        for rel in files:
            path = (self.root / rel).resolve()
            if not path.is_relative_to(self.root / 'event-log') or not path.is_file():
                raise IncompleteSource('Tracked specification missing', code='github_file_missing')
            body = path.read_text(encoding='utf8')
            title = next((line[2:].strip() for line in body.splitlines() if line.startswith('# ')), path.stem)
            metadata = re.split(r'(?m)^## ', clean(body), maxsplit=1)[0]
            platform_line = re.search(r'(?m)^\s*(?:-\s*)?플랫폼\s*:\s*(.*)', metadata)
            platforms = re.findall(r'\b(?:WEB|ANDROID|IOS)\b', platform_line.group(1).upper()) if platform_line else []
            service = rel.split('/')[1]
            counts[service] = counts.get(service, 0) + 1
            pages.append(dict(id=rel, url='https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/' + self.revision + '/' + quote(rel, safe='/'),
                              title=title, service=service, platforms=platforms, text=body, is_row=True,
                              unresolved='forced_update' in body and ('__app_update__exit' in body or 'forced_update_exit' in body)))
        return dict(pages=pages, databases=counts, row_count=len(pages), complete=True,
                    source_kind='github', source_revision=self.revision)
