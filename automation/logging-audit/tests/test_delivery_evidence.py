import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from koin_weekly_audit.notify import send_once, slack_payload, slack_text
from test_slack_payload import report


WEBHOOK = 'https://hooks.slack.com/services/test/redacted/example'


class DeliveryEvidenceTest(unittest.TestCase):
    def test_receipt_tracks_payload_and_time_and_reuse_is_not_a_post(self):
        response = MagicMock(status=200)
        response.read.return_value = b'ok'
        response.__enter__.return_value = response
        with tempfile.TemporaryDirectory() as folder:
            receipt = Path(folder) / 'receipt.json'
            with patch('urllib.request.urlopen', return_value=response) as request:
                first = send_once(WEBHOOK, {'text': 'hello'}, receipt)
                same = send_once(WEBHOOK, {'text': 'hello'}, receipt)
                changed = send_once(WEBHOOK, {'text': 'changed'}, receipt)
            self.assertEqual(request.call_count, 1)
            self.assertEqual(first['status'], 'sent')
            self.assertTrue(first['sent_at'])
            self.assertEqual(len(first['payload_sha256']), 64)
            self.assertTrue(same['reused'])
            self.assertTrue(same['payload_matches'])
            self.assertEqual(same['sent_at'], first['sent_at'])
            self.assertFalse(changed['payload_matches'])
            self.assertNotIn(WEBHOOK, receipt.read_text())
            self.assertNotIn('hello', receipt.read_text())

    def test_old_sent_receipt_is_not_proof_of_current_payload(self):
        with tempfile.TemporaryDirectory() as folder:
            receipt = Path(folder) / 'receipt.json'
            receipt.write_text(json.dumps({'status': 'sent'}))
            with patch('urllib.request.urlopen') as request:
                result = send_once(WEBHOOK, 'new contents', receipt)
            request.assert_not_called()
            self.assertTrue(result['reused'])
            self.assertFalse(result['payload_matches'])

    def test_ai_failure_and_actual_spec_source_visible_without_changing_findings(self):
        result = report()
        result['source_kind'] = 'github'
        result['agent'] = {'status': 'failed', 'failure_type': 'APIError'}
        result['normalization'] = {'android_debug_events': 1624}
        message = slack_text('stage', result['start'], result['end'], result)
        self.assertIn('AI 추가 조사: 미완료', message)
        self.assertIn('GitHub main · Notion 직접 대조 미실행', message)
        self.assertIn('디버그 1624건', message)
        self.assertIn('Android: 이상 없음', message)
        self.assertNotIn('APIError', message)
        self.assertIn('AI 추가 조사: 미완료', json.dumps(slack_payload('stage', result['start'], result['end'], result), ensure_ascii=False))

    def test_quota_is_ai_status_not_platform_logging_anomaly(self):
        result = report()
        result['agent'] = dict(status='failed', failure_diagnostics=dict(category='quota'))
        message = slack_text('stage', result['start'], result['end'], result)
        self.assertIn('사용량·결제 한도 확인 필요', message)
        self.assertIn('Android: 이상 없음', message)


if __name__ == '__main__':
    unittest.main()
