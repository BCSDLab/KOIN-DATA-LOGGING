import tempfile
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


if __name__ == '__main__':
    unittest.main()
