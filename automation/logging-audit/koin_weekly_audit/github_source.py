"""Read every tracked specification from the workflow's pinned main checkout."""
import os
import json
import hashlib
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

    def _document_index(self, tracked_files):
        base = self.root / '_archive/updates/2026-11-27/notion-sync'
        summary_path = base / 'summary.json'
        if not summary_path.is_file():
            return None  # Support older checkouts and small isolated test fixtures.
        try:
            summary = json.loads(summary_path.read_text(encoding='utf8'))
            entries = []
            for service in summary['services']:
                path = (base / service['path']).resolve()
                if not path.is_relative_to(base):
                    raise ValueError('Manifest escapes its directory')
                entries.extend(json.loads(path.read_text(encoding='utf8'))['pages'])
            extra_path = self.root / 'docs/current/additional-notion-pages.json'
            if extra_path.is_file():
                entries.extend(item['manifest'] for item in json.loads(extra_path.read_text(encoding='utf8'))['pages'])
            index = {item['path']: item for item in entries}
            if len(index) != len(entries) or not index:
                raise ValueError('Duplicate or empty document index')
            updates_path = self.root / 'docs/current/notion-page-updates.json'
            if updates_path.is_file():
                seen_updates = set()
                for update in json.loads(updates_path.read_text(encoding='utf8'))['pages']:
                    item, source = update['manifest'], update['source']
                    previous = index.get(item['path'])
                    if (not previous or item['notion_id'] in seen_updates or
                            previous['notion_id'] != item['notion_id'] or source['id'] != item['notion_id']):
                        raise ValueError('Invalid current page update identity')
                    seen_updates.add(item['notion_id'])
                    index[item['path']] = item
            for rel, item in index.items():
                if not rel.startswith('event-log/') or not rel.endswith('.md') or Path(rel).name == 'README.md':
                    raise ValueError('Invalid canonical document path')
                if not re.fullmatch(r'[a-f0-9]{64}', item['output_sha256']):
                    raise ValueError('Canonical document hash missing')
            tracked = set(tracked_files)
            if set(index) - tracked:
                raise IncompleteSource('Canonical specification missing', code='github_manifest_missing')
            aliases = {item['previous_path'] for item in summary.get('previous_exports', [])}
            if tracked - set(index) - aliases:
                raise IncompleteSource('Unexpected reader document', code='github_manifest_unexpected_file')
            return index
        except (OSError, KeyError, TypeError, ValueError) as exc:
            raise IncompleteSource('Canonical document manifest invalid', code='github_manifest_invalid') from exc

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
        reader_document_count = len(files)
        document_index = self._document_index(files)
        if document_index is not None:
            files = sorted(document_index)
        services = {p.split('/')[1] for p in files}
        if len(files) < 700 or len(services) < 21:
            raise IncompleteSource('GitHub specification scope reduced', code='github_scope_reduced')
        pages, counts = [], {}
        for rel in files:
            path = (self.root / rel).resolve()
            if not path.is_relative_to(self.root / 'event-log') or not path.is_file():
                raise IncompleteSource('Tracked specification missing', code='github_file_missing')
            raw = path.read_bytes()
            if document_index is not None and hashlib.sha256(raw).hexdigest() != document_index[rel]['output_sha256']:
                raise IncompleteSource('Canonical specification content changed', code='github_manifest_content_mismatch')
            body = raw.decode('utf8')
            title = next((line[2:].strip() for line in body.splitlines() if line.startswith('# ')), path.stem)
            metadata = re.split(r'(?m)^## ', clean(body), maxsplit=1)[0]
            platform_line = re.search(r'(?m)^\s*(?:-\s*)?플랫폼\s*:\s*(.*)', metadata)
            platforms = re.findall(r'\b(?:WEB|ANDROID|IOS)\b', platform_line.group(1).upper()) if platform_line else []
            service = rel.split('/')[1]
            counts[service] = counts.get(service, 0) + 1
            pages.append(dict(id=rel, url='https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/' + self.revision + '/' + quote(rel, safe='/'),
                              title=title, service=service, platforms=platforms, text=body, is_row=True,
                              notion_id=document_index[rel].get('notion_id') if document_index is not None else None,
                              unresolved='forced_update' in body and ('__app_update__exit' in body or 'forced_update_exit' in body)))
        return dict(pages=pages, databases=counts, row_count=len(pages), complete=True,
                    source_kind='github', source_revision=self.revision,
                    canonical_index_used=document_index is not None,
                    ignored_reference_documents=reader_document_count - len(files))
