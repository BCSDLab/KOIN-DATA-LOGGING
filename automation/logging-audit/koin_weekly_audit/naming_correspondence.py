"""Verified Android release names and their current specification counterparts.

These are review evidence, not accepted aliases: the original label must still
produce a mismatch. Do not infer deployment cutovers or rewrite source events.
"""
RELEASE = '41071baf8465e0083f156da61a80b30296c63715'
PREFIX = 'https://github.com/BCSDLab/KOIN_ANDROID/blob/' + RELEASE + '/'
CORE = 'core/analytics/src/main/java/in/koreatech/koin/core/analytics/'
CORRESPONDENCES = {
    'board__main_category__lost_item_entry__category_entry__click': {
        'current_label': 'board__main_category__category_navigation__lost_item_entry__click',
        'source_url': PREFIX + CORE + 'LostAndFoundAnalyticsConstant.kt#L7'},
    'main__main__bus_entry__search_entry__click': {
        'current_label': 'bus__main__bus_entry__search_entry__click',
        'source_url': PREFIX + CORE + 'HomeEventLabels.kt#L15'},
    'main__main__bus_entry__ticket_entry__click': {
        'current_label': 'ticket__main__bus_entry__ticket_entry__click',
        'source_url': PREFIX + CORE + 'HomeEventLabels.kt#L12'},
    'real_estate__main_category__real_estate_entry__category_entry__click': {
        'current_label': 'real_estate__main_category__category_navigation__real_estate_entry__click',
        'source_url': PREFIX + CORE + 'RealEstateAnalyticsConstant.kt#L4'},
    'shop__main_category__shop_entry__category_entry__click': {
        'current_label': 'shop__main_category__category_navigation__shop_entry__click',
        'source_url': PREFIX + CORE + 'ShopAnalyticsConstant.kt#L6'},
}


def for_observation(catalog, observation):
    if (observation.get('platform') != 'ANDROID' or observation.get('app_version') != '5.2.4'
            or observation.get('event_name') not in ('DA1', 'DA2')):
        return None
    entry = CORRESPONDENCES.get(observation.get('event_label'))
    if not entry or entry['current_label'] in catalog['conflicts']:
        return None
    contracts = catalog['by_label'].get(entry['current_label'], [])
    if not any('ANDROID' in c['platforms'] for c in contracts):
        return None
    return dict(entry, platform='ANDROID', app_version='5.2.4', accepted_alias=False)
