import unittest
from koin_weekly_audit.contracts import build_catalog,compare
from koin_weekly_audit.naming_correspondence import CORRESPONDENCES
from koin_weekly_audit.notify import detail_markdown
from koin_weekly_audit.investigation import investigate
from test_weekly_audit import page,OBS


class NamingCorrespondenceTest(unittest.TestCase):
    def fixture(self,old_label):
        current=CORRESPONDENCES[old_label]['current_label'];screen=current.split('__')[1]
        text=f'- 새 로깅\n- event_name: DA1\n- event_label: {current}\n- screen_view: {screen}\n- event_category: click\n- value: 확인'
        p=page(text,['ANDROID']);p['url']='https://github.com/BCSDLab/KOIN-DATA-LOGGING/blob/sha/event-log/spec.md'
        obs=dict(OBS,platform='ANDROID',app_version='5.2.4',event_label=old_label,screen_view=screen,value='확인')
        return build_catalog([p]),obs,current

    def test_all_five_names_stay_mismatches_with_current_source_links(self):
        for old_label in CORRESPONDENCES:
            with self.subTest(label=old_label):
                cat,obs,target=self.fixture(old_label);r=compare(cat,[obs])
                self.assertEqual([f['reason'] for f in r['findings']],['previous_naming_label'])
                f=r['findings'][0];self.assertEqual(f['label'],old_label);self.assertEqual(f['field'],'event_label')
                self.assertEqual(f['expected_values'],[target]);self.assertTrue(f['specification_urls'])
                self.assertFalse(f['naming_correspondence']['accepted_alias'])
                self.assertIn(target,r['unobserved_labels'])
                self.assertEqual(compare(cat,[dict(obs,event_label=target)])['findings'],[])
                r.update(complete=True)
                analysis=investigate(cat,r,[obs])['investigations'][0]
                self.assertTrue(analysis['contracts'])
                self.assertEqual(analysis['naming_correspondence']['current_label'],target)

    def test_other_field_failures_stay_visible(self):
        old=next(iter(CORRESPONDENCES));cat,obs,target=self.fixture(old)
        r=compare(cat,[dict(obs,event_name='DA2',screen_view='wrong',event_category='scroll',value=None)])
        self.assertEqual({f['reason'] for f in r['findings']},{'previous_naming_label','event_name_mismatch','screen_view_mismatch','event_category_mismatch','value_missing'})
        for f in r['findings']:self.assertTrue(f['specification_urls'])
        self.assertEqual(next(f for f in r['findings'] if f['reason']=='event_name_mismatch')['expected_values'],['DA1'])
        r.update(complete=True,start='2026-11-23',end='2026-11-27')
        self.assertIn('정상 별칭으로 허용한 것은 아닙니다',detail_markdown({'stage':r}))

    def test_other_platforms_versions_and_unknown_names_are_not_guessed(self):
        old=next(iter(CORRESPONDENCES));cat,obs,_=self.fixture(old)
        for changes in [dict(platform='IOS'),dict(platform='WEB'),dict(app_version='5.2.3'),dict(event_label='unknown__main__target__click')]:
            self.assertIn('unregistered_label',{f['reason'] for f in compare(cat,[dict(obs,**changes)])['findings']})
        self.assertEqual(compare(build_catalog([]),[obs])['findings'][0]['reason'],'unregistered_label')

    def test_photo_mobile_label_touching_korean_text_is_not_dropped(self):
        text='''- 새 로깅
- 설명: 사진 넘기기
- event_name: DA1
- screen_view: room_detail
- event_label:
  - 웹 real_estate__room_detail__photo_view__slide__click
  - 모바일real_estate__room_detail__photo_view__slide__swipe
- event_category:
  - 웹: click
  - 모바일: swipe
- value: 이전 / 다음'''
        cat=build_catalog([page(text,['WEB'])]);click='real_estate__room_detail__photo_view__slide__click';swipe=click[:-5]+'swipe'
        self.assertEqual(set(cat['by_label']),{click,swipe})
        self.assertEqual(cat['by_label'][click][0]['status'],'current')
        self.assertEqual(cat['by_label'][swipe][0]['status'],'unresolved')
        for platform in ['ANDROID','IOS','WEB']:
            r=compare(cat,[dict(OBS,platform=platform,event_label=swipe,event_category='swipe',screen_view='room_detail',value='다음')])
            self.assertEqual([f['reason'] for f in r['findings']],['specification_conflict'])
            self.assertEqual(r['findings'][0]['specification_urls'],['https://www.notion.so/test'])
        self.assertEqual(compare(cat,[dict(OBS,platform='WEB',event_label=click,screen_view='room_detail',value='다음')])['findings'],[])
