import copy
import json
import os
import tempfile
import unittest
from datetime import date
from types import SimpleNamespace as NS
from unittest.mock import patch

from koin_weekly_audit.agent import EvidenceTools, InvestigationError, investigate, validate_output
from koin_weekly_audit.contracts import build_catalog, compare
from koin_weekly_audit.notify import slack_text
from run import audit
from test_runner import Collector


LABEL = 'test__screen__button__click'


def fixture():
    catalog = build_catalog(Collector().collect()['pages'])
    rows = [dict(event_date='20261120', event_label=LABEL, platform='IOS', app_version='5.2.6',
                 event_name='DA2', screen_view='wrong_screen', event_category='click', value='PRIVATE RAW VALUE',
                 event_count=4, duplicate_param_keys=0)]
    report = compare(catalog, rows)
    report.update(complete=True, environment='stage', start='2026-11-16', end='2026-11-22', query_job_id='job1')
    return catalog, report, rows


def output(ref='E2'):
    return json.dumps(dict(investigations=[dict(observation='IOS 5.2.6에서 4건 관측',
                      hypothesis='배포 버전별 계약 차이 가능성', next_action='담당자가 배포 시점을 확인', evidence_ids=[ref])],
                      limitations=['중요 항목 표본 조사이며 원인 확정이 아닙니다.']))


class FakeSessions:
    def __init__(self, complete=True, invalid_tool=False, text=None, missing_text=False):
        self.complete, self.invalid_tool = complete, invalid_tool
        self.sent, self.deleted, self.options = [], [], None
        self.events = NS(create=lambda sid, events: self.sent.extend(events))
        self.turns = NS(list=lambda *a, **kw: NS(data=[dict(id='t1', status='waiting')]))
        self.items = NS(list=lambda *a, **kw: [] if missing_text else [dict(type='message', role='assistant',
            turn_id='t1', phase='final_answer', status='completed', content=[dict(type='output_text', text=text or output())])])

    def create(self, **kwargs):
        self.options = kwargs
        return self

    def __enter__(self): return self
    def __exit__(self, *args): pass
    def __iter__(self):
        yield dict(type='agent.session.created', session=dict(id='s1'))
        yield dict(type='agent.session.requires_action', session=dict(id='s1'))
        yield dict(type='agent.session.idle')
        if self.complete:
            yield dict(type='agent.session.turn.completed', turn=dict(id='t1', session_id='s1', subagent_id=None), usage=dict(input_tokens=12, output_tokens=10))

    def retrieve(self, sid):
        def action(name, args, number):
            return dict(type='function_call', turn_id='t1', call_id='c' + str(number), name=name, arguments=args)
        return dict(required_actions=[
            action('shell' if self.invalid_tool else 'list_findings', dict(platform='IOS', offset=0), 1),
            action('breakdown', dict(label=LABEL, platform='IOS', group_by='app_version'), 2),
            action('read_contract', dict(label=LABEL), 3)])

    def delete(self, sid): self.deleted.append(sid)


def client(sessions):
    return NS(beta=NS(agents=NS(sessions=sessions)))


class AgentTest(unittest.TestCase):
    def test_managed_turn_tools_and_grounded_output(self):
        catalog, report, rows = fixture()
        before = copy.deepcopy(report)
        sessions = FakeSessions()
        result = investigate(catalog, report, rows, client(sessions))
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['tool_calls'], 3)
        self.assertEqual(result['cleanup_status'], 'deleted')
        self.assertEqual(sessions.options['environment'], {'type': 'none'})
        self.assertEqual(result['evidence'][1]['data']['groups'], [dict(key='5.2.6', events=4)])
        contract = result['evidence'][2]['data']['current'][0]
        self.assertEqual(contract['names'], ['DA1'])
        self.assertEqual(contract['screens'], ['screen'])
        self.assertNotIn('PRIVATE RAW VALUE', json.dumps(result))
        self.assertNotIn('fixed_value', contract)
        self.assertEqual(before, report)
        self.assertEqual(sessions.deleted, ['s1'])

    def test_idle_not_completion_and_cancel_cleanup(self):
        sessions = FakeSessions(complete=False)
        result = investigate(*fixture(), client=client(sessions))
        self.assertEqual(result['failure_code'], 'TurnCompletionUnconfirmed')
        self.assertEqual(sessions.sent[-1]['type'], 'agent.session.input.cancel')
        self.assertEqual(sessions.deleted, ['s1'])

    def test_unknown_tool_rejected_before_side_effect(self):
        sessions = FakeSessions(invalid_tool=True)
        result = investigate(*fixture(), client=client(sessions))
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['failure_code'], 'InvalidToolArguments')
        self.assertFalse(any(x['type'].endswith('tool_result') for x in sessions.sent))

    def test_invented_evidence_and_missing_final_rejected(self):
        result = investigate(*fixture(), client=client(FakeSessions(text=output('E999'))))
        self.assertEqual(result['failure_code'], 'UnknownEvidence')
        result = investigate(*fixture(), client=client(FakeSessions(missing_text=True)))
        self.assertEqual(result['status'], 'failed')

    def test_budget_and_query_injection_blocked(self):
        tools = EvidenceTools(*fixture(), limit=1)
        tools.call('breakdown', dict(label=LABEL, platform='IOS', group_by='app_version'))
        with self.assertRaises(InvestigationError):
            tools.call('read_contract', dict(label=LABEL))
        tools = EvidenceTools(*fixture())
        with self.assertRaises(InvestigationError):
            tools.call('breakdown', dict(label=LABEL, platform='IOS', group_by='app_version; DROP TABLE x'))
        with self.assertRaises(InvestigationError):
            tools.call('breakdown', dict(label='unknown', platform='IOS', group_by='event_date'))

    def test_missing_key_and_incomplete_audit(self):
        catalog, report, rows = fixture()
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(investigate(catalog, report, rows)['failure_type'], 'OpenAIKeyMissing')
        report['complete'] = False
        self.assertEqual(investigate(catalog, report, rows)['status'], 'skipped')

    def test_missing_label_aggregates_actual_missing_rows(self):
        catalog, report, rows = fixture()
        rows[0]['event_label'] = None
        report = compare(catalog, rows)
        tools = EvidenceTools(catalog, report, rows)
        result = tools.call('breakdown', dict(label='(missing)', platform='IOS', group_by='app_version'))
        self.assertEqual(result['data']['total_events'], 4)

    def test_api_error_does_not_expose_key_or_fake_success(self):
        sessions = FakeSessions()
        def broken(**kw): raise PermissionError('sk-proj-DO-NOT-PRINT')
        sessions.create = broken
        result = investigate(*fixture(), client=client(sessions))
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['failure_type'], 'PermissionError')
        self.assertNotIn('sk-proj', json.dumps(result))

    def test_cancel_failure_still_attempts_delete_and_checkpoints_id(self):
        sessions, saved = FakeSessions(complete=False), []
        original = sessions.events.create
        def events(sid, events):
            if events[0]['type'].endswith('.cancel'): raise RuntimeError('no connection')
            original(sid, events)
        sessions.events.create = events
        result = investigate(*fixture(), client=client(sessions), checkpoint=lambda r: saved.append(copy.deepcopy(r)))
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['cancel_status'], 'unconfirmed')
        self.assertEqual(sessions.deleted, ['s1'])
        self.assertTrue(any(r.get('session_id') == 's1' for r in saved))

    def test_wall_time_bounded_and_cancelled(self):
        ticks = iter([0, 181])
        sessions = FakeSessions()
        result = investigate(*fixture(), client=client(sessions), clock=lambda: next(ticks))
        self.assertEqual(result['failure_code'], 'InvestigationTimeout')
        self.assertEqual(result['cleanup_status'], 'deleted')

    def test_slack_preserves_rules_and_marks_ai_failure(self):
        catalog, report, rows = fixture()
        report['agent'] = dict(status='failed', failure_type='PermissionDeniedError')
        message = slack_text('stage', report['start'], report['end'], report)
        self.assertNotIn('PermissionDeniedError', message)
        self.assertIn('이상·확인 필요', message)
        self.assertIn('1개 label', message)
        report['agent'] = investigate(catalog, report, rows, client(FakeSessions()))
        completed = slack_text('stage', report['start'], report['end'], report)
        self.assertEqual(message.split('AI 추가 조사:')[0], completed.split('AI 추가 조사:')[0])
        self.assertIn('AI 추가 조사: 미완료', message)
        self.assertIn('AI 추가 조사: 완료', completed)

    def test_runner_agent_failure_isolated_and_reported(self):
        def query(*args, **kw):
            return dict(rows=[dict(r, platform='ANDROID', app_version='5.2.4') for r in fixture()[2]], complete=True, missing_daily_tables=[])
        calls = []
        def investigator(catalog, report, rows):
            calls.append((report['environment'], len(rows)))
            if report['environment'] == 'stage': raise RuntimeError('DO NOT PRINT SECRET')
            return dict(status='completed', analysis=json.loads(output()), evidence=[])
        with tempfile.TemporaryDirectory() as folder:
            reports = audit(date(2026, 11, 16), folder, folder + '/state', collector=Collector(),
                            query=query, investigator=investigator)
            self.assertTrue(reports['stage']['complete'])
            self.assertEqual(reports['stage']['agent']['status'], 'failed')
            self.assertEqual(reports['production']['agent']['status'], 'completed')
            self.assertEqual(calls, [('stage', 1), ('production', 1)])
            self.assertNotIn('DO NOT PRINT SECRET', json.dumps(reports))


if __name__ == '__main__': unittest.main()
