"""Bounded live test using only a synthetic contract; no BigQuery or Slack."""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI
from koin_weekly_audit.agent import investigate, failure_diagnostics
from koin_weekly_audit.contracts import build_catalog, compare


def main():
    output = Path('reports/api-smoke.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog([dict(title='API 시험용 합성 계약', service='synthetic',
        url='https://github.com/BCSDLab/KOIN-DATA-LOGGING', platforms=['ANDROID'],
        text='- 새 로깅\n- screen_view: screen\n- event_name: DA1\n'
             '- event_label: test__screen__button__click\n- event_category: click\n- value: 확인')])
    rows = [dict(event_date='20261120', event_name='DA2_debug',
        event_label='test__screen__button__click (debug)', event_category='click_debug',
        screen_view='screen', value='확인', event_count=2, platform='ANDROID', app_version='5.2.4')]
    report = compare(catalog, rows)
    report.update(complete=True, environment='synthetic', start='2026-11-16', end='2026-11-22')
    result = dict(tested_at=datetime.now(timezone.utc).isoformat(), synthetic_only=True,
                  slack_sent=False, bigquery_called=False, model=os.getenv('OPENAI_AGENT_MODEL', 'gpt-6-astra'))
    def diagnose(exc):
        # This path contains synthetic inputs only. Never enable raw messages for real audits.
        text = str(exc)
        secret = os.getenv('OPENAI_API_KEY')
        if secret:
            text = text.replace(secret, '[redacted]')
        text = re.sub(r'(?i)(?:sk-[A-Za-z0-9_-]+|Bearer\s+\S+|https?://\S+)', '[redacted]', text)
        text = re.sub(r'[A-Za-z0-9_-]{32,}', '[identifier]', text)
        result['synthetic_error_message'] = text[:1500]
        body = getattr(exc, 'body', None)
        result['error_body_keys'] = sorted(str(key)[:40] for key in body) if isinstance(body, dict) else []
    with OpenAI(max_retries=0, timeout=30) as client:
        try:
            model = client.models.retrieve(result['model'])
            result['model_access'] = dict(status='available', id=model.id)
        except Exception as exc:
            result['model_access'] = dict(status='failed', failure_type=type(exc).__name__,
                                           diagnostics=failure_diagnostics(exc))
        result['agent'] = investigate(catalog, report, rows, client=client, failure_observer=diagnose,
            checkpoint=lambda agent: output.write_text(json.dumps(dict(result, agent=agent), ensure_ascii=False, indent=2), encoding='utf8'))
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['agent'].get('status') == 'completed' and result['agent'].get('cleanup_status') == 'deleted' else 1


if __name__ == '__main__':
    raise SystemExit(main())
