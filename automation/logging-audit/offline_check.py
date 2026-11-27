"""Exercise the complete reporting path with synthetic inputs and no network."""
import json
from datetime import date
from pathlib import Path
from unittest.mock import patch
from run import audit
from koin_weekly_audit.notify import detail_markdown


class SyntheticSource:
    def collect(self):
        return dict(complete=True, source_kind='synthetic', row_count=836,
            databases={str(i): 1 for i in range(22)},
            pages=[dict(title='합성 시험용 계약', service='synthetic',
                url='https://github.com/BCSDLab/KOIN-DATA-LOGGING',
                platforms=['IOS', 'ANDROID', 'WEB'],
                text='- 새 로깅\n- screen_view: screen\n- event_name: DA1\n'
                     '- event_label: demo__screen__button__click\n- value: 확인\n- event_category: click')])


def synthetic_query(project, *args, **kwargs):
    common = dict(event_date='20261118', event_name='DA1', event_label='demo__screen__button__click',
                  screen_view='screen', event_category='click', value='확인', value_parameter_present=True)
    rows = [dict(common, platform='ANDROID', app_version='5.2.4', event_count=2,
                 event_name='DA2_debug', event_label=common['event_label'] + ' (debug)', event_category='click_debug'),
            dict(common, platform='IOS', app_version='5.2.6' if project.startswith('koin-stage') else '5.2.5',
                 event_count=3, value=None),
            dict(common, platform='WEB', app_version=None, event_count=4, event_label='unknown__screen__button__click')]
    return dict(rows=rows, complete=True, missing_daily_tables=[])


def main():
    with patch('run.summary_url', return_value=None), \
         patch('urllib.request.urlopen', side_effect=AssertionError('Network disabled')) as http, \
         patch('socket.socket', side_effect=AssertionError('Network disabled')) as sockets:
        reports = audit(date(2026, 11, 16), 'reports', '.offline-state',
                        collector=SyntheticSource(), query=synthetic_query, send=False)
        http.assert_not_called()
        sockets.assert_not_called()
    for report in reports.values():
        assert report['complete'] and report['events'] == 9
        assert report['delivery_status'] == 'not_requested'
        assert report['investigation']['status'] == 'completed'
        assert report['investigation']['external_ai_called'] is False
        assert len(report['investigation']['investigations']) == 3
    Path('reports/offline-detail.md').write_text(detail_markdown(reports), encoding='utf8')
    result = dict(synthetic_only=True, external_ai_called=False, external_data_queried=False, slack_sent=False,
        environments={environment: dict(events=report['events'], status=report['investigation']['status'],
            investigated=len(report['investigation']['investigations'])) for environment, report in reports.items()})
    Path('reports/offline-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
