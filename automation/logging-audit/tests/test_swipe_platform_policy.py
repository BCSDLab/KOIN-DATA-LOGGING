import unittest
from koin_weekly_audit.contracts import build_catalog,compare,platform_scopes
from test_weekly_audit import page,OBS


class SwipePlatformPolicyTest(unittest.TestCase):
    def test_mixed_page_keeps_web_click_and_ios_swipe_separate(self):
        click='real_estate__room_detail__photo_view__slide__click';swipe=click[:-5]+'swipe'
        text=f'''### 플랫폼별 계약 범위
| event_label | platform |
| --- | --- |
| `{click}` | WEB |
| `{swipe}` | IOS |

## 새 로깅
- screen_view: room_detail
- event_name: DA1
- event_label: 웹 {click} 모바일{swipe}
- event_category: 웹 click 모바일 swipe
- value: 이전 / 다음'''
        cat=build_catalog([page(text,['IOS','WEB'])])
        self.assertEqual(cat['by_label'][click][0]['platforms'],['WEB'])
        self.assertEqual(cat['by_label'][swipe][0]['platforms'],['IOS'])
        for label,category,valid in [(click,'click','WEB'),(swipe,'swipe','IOS')]:
            for platform in ['IOS','ANDROID','WEB']:
                result=compare(cat,[dict(OBS,platform=platform,event_label=label,event_category=category,screen_view='room_detail',value='다음')])
                self.assertEqual([f['reason'] for f in result['findings']],[] if platform==valid else ['platform_mismatch'])

    def test_swipe_definition_cannot_allow_android_or_web_by_accident(self):
        text='## 새 로깅\n- screen_view: screen\n- event_name: DA1\n- event_label: shop__screen__navigation__back__swipe\n- event_category: swipe\n- value: 뒤로가기'
        cat=build_catalog([page(text,['ANDROID','IOS','WEB'])]);contract=next(iter(cat['by_label'].values()))[0]
        self.assertEqual(contract['platforms'],['IOS'])
        self.assertEqual(contract['status'],'unresolved')

    def test_unconfirmed_click_is_not_implicitly_added_to_swipe_platform(self):
        click='callvan__callvan_notification__notification_list__delete__click';swipe=click[:-5]+'swipe'
        text=f'''### 플랫폼별 계약 범위
| event_label | platform |
| --- | --- |
| {click} | 미확정 |
| {swipe} | IOS |

## 새 로깅
- screen_view: callvan_notification
- event_name: DA2
- event_label: {click} / {swipe}
- event_category: click / swipe
- value: 알림 삭제'''
        cat=build_catalog([page(text,['IOS'])])
        self.assertEqual(cat['by_label'][click][0]['platforms'],[])
        self.assertEqual(cat['by_label'][click][0]['status'],'unresolved')
        self.assertEqual(cat['by_label'][swipe][0]['status'],'current')

    def test_duplicate_explicit_scope_is_rejected(self):
        text='### 플랫폼별 계약 범위\n| shop__screen__back__swipe | IOS |\n| shop__screen__back__swipe | ANDROID |'
        with self.assertRaises(ValueError):platform_scopes(text)
