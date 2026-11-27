"""Guard the no-paid-AI requirement across code, dependency and workflow paths."""
import ast
import unittest
from pathlib import Path

from koin_weekly_audit.bigquery_source import build_query


ROOT = Path(__file__).resolve().parents[1]


class NoAIRuntimeTest(unittest.TestCase):
    def test_runtime_has_no_ai_sdk_or_endpoint(self):
        files = list((ROOT/'koin_weekly_audit').glob('*.py')) + [ROOT/'run.py', ROOT/'offline_check.py']
        for path in files:
            source = path.read_text()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    self.assertFalse(any(alias.name.split('.')[0] in ('openai', 'anthropic', 'litellm') for alias in node.names), path.name)
                elif isinstance(node, ast.ImportFrom):
                    self.assertNotIn((node.module or '').split('.')[0], ('openai', 'anthropic', 'litellm'), path.name)
            self.assertNotIn('api.openai.com', source)
        self.assertFalse((ROOT/'api_smoke.py').exists())
        self.assertFalse((ROOT/'koin_weekly_audit'/'agent.py').exists())

    def test_dependencies_and_workflow_do_not_pass_ai_credentials(self):
        requirements = (ROOT/'requirements.txt').read_text().lower()
        self.assertNotIn('openai', requirements)
        workflow = (ROOT.parents[1]/'.github/workflows/weekly-logging-audit.yml').read_text()
        self.assertNotIn('OPENAI', workflow)
        self.assertNotIn('api_smoke', workflow)
        self.assertIn('offline_check', workflow)

    def test_debug_query_can_find_missing_label_without_label_filter(self):
        sql = build_query('kap-chat', 'analytics_432041405')
        self.assertIn("platform = 'ANDROID' AND (event_name IN ('DA1_debug','DA2_debug')", sql)
        self.assertIn("'CAMPUS_DEBUG','BUSINESS_DEBUG','USER_DEBUG'", sql)


if __name__ == '__main__':
    unittest.main()
