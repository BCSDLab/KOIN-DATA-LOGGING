import tempfile
import json
import hashlib
import unittest
from pathlib import Path

from koin_weekly_audit.github_source import GitHubSource
from koin_weekly_audit.notion_source import IncompleteSource
from koin_weekly_audit.contracts import build_catalog


class GitHubSourceTest(unittest.TestCase):
    def test_all_tracked_documents_and_pinned_links(self):
        body = '''# 뒤로가기
플랫폼: IOS
## 새 로깅
- screen\\_view: <code>room_common</code>
- event\\_name: <code>DA1</code>
- event\\_label: <code>real_estate__room_common__navigation__back__click</code>
- event\\_category: <code>click</code>
- value: 뒤로가기
'''
        with tempfile.TemporaryDirectory() as folder:
            paths = [f'event-log/{i % 21:02d}-서비스/{i}.md' for i in range(700)]
            for rel in paths:
                p = Path(folder, rel)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body, encoding='utf8')
            result = GitHubSource(folder, 'a'*40, paths).collect()
            self.assertEqual(result['row_count'], 700)
            self.assertEqual(len(result['databases']), 21)
            self.assertEqual(result['pages'][0]['platforms'], ['IOS'])
            catalog = build_catalog(result['pages'])
            contract = catalog['by_label']['real_estate__room_common__navigation__back__click'][0]
            self.assertEqual(contract['names'], ['DA1'])
            self.assertIn('/blob/' + 'a'*40 + '/', contract['url'])
            Path(folder, paths[-1]).unlink()
            with self.assertRaises(IncompleteSource):
                GitHubSource(folder, 'a'*40, paths).collect()

    def test_reduced_scope_and_missing_revision_fail_closed(self):
        for revision, paths in (('', []), ('a'*40, ['event-log/service/one.md'])):
            with self.assertRaises(IncompleteSource):
                GitHubSource('.', revision, paths).collect()



class CanonicalGitHubSourceTest(unittest.TestCase):
    def setup_repo(self, folder):
        root = Path(folder)
        paths = [f'event-log/{i % 21:02d}-서비스/{i}.md' for i in range(700)]
        body = '# Sample\n플랫폼: IOS\n## 새 로깅\n- event_name: DA1\n'
        for rel in paths:
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding='utf8')
        base = root / '_archive/updates/2026-11-27/notion-sync'
        base.mkdir(parents=True)
        entries = [dict(path=rel, notion_id=str(i).zfill(32),
                        output_sha256=hashlib.sha256(body.encode()).hexdigest()) for i, rel in enumerate(paths)]
        (base / 'service.json').write_text(json.dumps(dict(pages=entries)), encoding='utf8')
        alias = 'event-log/00-서비스/old-reference.md'
        (root / alias).write_text('# 이전 원본 안내\n', encoding='utf8')
        (base / 'summary.json').write_text(json.dumps(dict(services=[dict(path='service.json')],
            previous_exports=[dict(previous_path=alias)])), encoding='utf8')
        return root, paths, alias

    def test_canonical_registry_excludes_preserved_reference_documents(self):
        with tempfile.TemporaryDirectory() as folder:
            root, paths, alias = self.setup_repo(folder)
            result = GitHubSource(root, 'a' * 40, paths + [alias]).collect()
            self.assertEqual(result['row_count'], 700)
            self.assertEqual(result['ignored_reference_documents'], 1)
            self.assertTrue(result['canonical_index_used'])
            self.assertTrue(all(p['id'] != alias for p in result['pages']))

    def test_missing_canonical_document_fails_with_aliases_present(self):
        with tempfile.TemporaryDirectory() as folder:
            root, paths, alias = self.setup_repo(folder)
            with self.assertRaisesRegex(IncompleteSource, 'Canonical specification missing'):
                GitHubSource(root, 'a' * 40, paths[:-1] + [alias]).collect()

    def test_unregistered_reader_document_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            root, paths, alias = self.setup_repo(folder)
            extra = 'event-log/00-서비스/unregistered.md'
            (root / extra).write_text('# 누락된 등록\n', encoding='utf8')
            with self.assertRaisesRegex(IncompleteSource, 'Unexpected reader document'):
                GitHubSource(root, 'a' * 40, paths + [alias, extra]).collect()

    def test_changed_canonical_value_fails_before_parsing(self):
        with tempfile.TemporaryDirectory() as folder:
            root, paths, alias = self.setup_repo(folder)
            (root / paths[0]).write_text('# Changed value\n', encoding='utf8')
            with self.assertRaisesRegex(IncompleteSource, 'Canonical specification content changed'):
                GitHubSource(root, 'a' * 40, paths + [alias]).collect()


if __name__ == '__main__':
    unittest.main()
