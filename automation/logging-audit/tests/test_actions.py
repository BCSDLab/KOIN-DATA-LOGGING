import io
import json
import unittest
from unittest.mock import patch

from koin_weekly_audit.actions import summary_url


class ActionsLinkTest(unittest.TestCase):
    def test_link_targets_current_attempt_job_summary(self):
        env = dict(GITHUB_REPOSITORY='BCSDLab/KOIN-DATA-LOGGING', GITHUB_RUN_ID='123',
                   GITHUB_RUN_ATTEMPT='2', GITHUB_JOB='audit', GH_ACTIONS_READ_TOKEN='PRIVATE')
        body = io.BytesIO(json.dumps({'jobs':[{'name':'audit', 'id':456}]}).encode())
        with patch.dict('os.environ', env, clear=True), patch('urllib.request.urlopen', return_value=body) as request:
            self.assertEqual(summary_url(), 'https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/123#summary-456')
            self.assertIn('/attempts/2/jobs', request.call_args.args[0].full_url)

    def test_metadata_failure_falls_back_without_exposing_credentials(self):
        env = dict(GITHUB_REPOSITORY='BCSDLab/KOIN-DATA-LOGGING', GITHUB_RUN_ID='123', GH_ACTIONS_READ_TOKEN='PRIVATE')
        with patch.dict('os.environ', env, clear=True), patch('urllib.request.urlopen', side_effect=OSError('PRIVATE')), patch('builtins.print') as output:
            self.assertTrue(summary_url().endswith('/123'))
            self.assertNotIn('PRIVATE', str(output.call_args))

    def test_no_actions_context_has_no_link(self):
        with patch.dict('os.environ', {}, clear=True):
            self.assertIsNone(summary_url())
