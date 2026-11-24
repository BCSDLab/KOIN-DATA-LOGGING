import unittest
from koin_weekly_audit.notify import slack_payload, slack_text, detail_markdown


def report(findings=None):
    return dict(complete=True, start='2026-11-16', end='2026-11-22', events=30,
                platform_summary={p: dict(events=10) for p in ('IOS','ANDROID','WEB')},
                source_revision='a'*40, findings=findings or [],
                detail_url='https://github.com/BCSDLab/KOIN-DATA-LOGGING/actions/runs/1')


def finding(label, reason='screen_view_mismatch', platform='IOS'):
    return dict(label=label, reason=reason, category='current_mismatch', count=3,
                platforms=[platform], platform_counts={platform:3}, platform_versions={platform:['5.2.6']},
                expected_values=['room_common'], platform_observed_values={platform:['room_detail']},
                specification_urls=['https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/'+'a'*40+'/event-log/spec.md'])


class SlackPayloadTest(unittest.TestCase):
    def test_normal_platforms_only_report_no_anomaly(self):
        r=report();r['agent']=dict(status='failed',failure_type='APIError')
        message=slack_text('stage',r['start'],r['end'],r)
        for p in ('iOS','Android','Web'): self.assertIn(p+': 이상 없음',message)
        self.assertNotIn('APIError',message)
        self.assertNotIn('문제 label 예시',message)

    def test_platform_anomalies_are_independent(self):
        r=report([finding('room__common__back__click')])
        message=slack_text('stage',r['start'],r['end'],r)
        self.assertIn('iOS: 이상·확인 필요 1개 label',message)
        self.assertIn('Android: 이상 없음',message)
        self.assertIn('Web: 이상 없음',message)
        payload=slack_payload('stage',r['start'],r['end'],r)
        self.assertIn('|상세보기>',str(payload['blocks']))

    def test_full_details_do_not_drop_labels_and_show_actual_expected(self):
        r=report([finding('room__screen__button'+str(i)+'__click') for i in range(30)])
        details=detail_markdown({'stage':r})
        for f in r['findings']: self.assertIn(f['label'],details)
        self.assertIn('room_common',details);self.assertIn('room_detail',details)
        self.assertIn('screen_view 불일치',details)
        self.assertIn('5.2.6',details)
        self.assertLess(len(slack_text('stage',r['start'],r['end'],r)),400)

    def test_zero_traffic_and_incomplete_are_not_healthy(self):
        r=report();r['platform_summary']['IOS']['events']=0
        self.assertNotIn('iOS: 이상 없음',slack_text('stage',r['start'],r['end'],r))
        r.update(complete=False,missing_daily_tables=['events_20261117'])
        payload=slack_payload('stage',r['start'],r['end'],r)
        self.assertIn('20261117',str(payload));self.assertNotIn('이상 없음',str(payload))

    def test_unobserved_contracts_are_not_anomalies(self):
        r=report();r['unobserved_labels']=['not_observed']
        self.assertNotIn('not_observed',slack_text('stage',r['start'],r['end'],r))
        self.assertIn('iOS: 이상 없음',slack_text('stage',r['start'],r['end'],r))

    def test_historical_unregistered_and_value_reasons_are_in_details(self):
        r=report([finding('old_log','historical_label_still_collected'),
                  finding('new_log','unregistered_label'),finding('value_log','fixed_value_mismatch')])
        r['findings'][2]['raw_value']='PRIVATE'
        details=detail_markdown({'production':r})
        for expected in ('과거 명세 label 수집','명세에 없는 label','고정 value 불일치'):
            self.assertIn(expected,details)
        self.assertNotIn('PRIVATE',details)


if __name__ == '__main__': unittest.main()
