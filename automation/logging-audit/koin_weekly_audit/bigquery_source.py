import re
from datetime import date, timedelta, datetime, timezone


def build_query(project, dataset, intraday_date=None):
    if not re.fullmatch(r'[a-z][a-z0-9-]+', project) or not re.fullmatch(r'[A-Za-z0-9_]+', dataset):
        raise ValueError('Invalid BigQuery identifier')
    if intraday_date is not None and not re.fullmatch(r'[0-9]{8}', intraday_date):
        raise ValueError('Invalid intraday date')
    suffix_filter = "_TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix AND REGEXP_CONTAINS(_TABLE_SUFFIX, r'^[0-9]{8}$')"
    if intraday_date:
        suffix_filter = "(" + suffix_filter + " OR _TABLE_SUFFIX = 'intraday_" + intraday_date + "')"
    def param(key):
        return "(SELECT ANY_VALUE(COALESCE(p.value.string_value, CAST(p.value.int_value AS STRING), CAST(p.value.double_value AS STRING), CAST(p.value.float_value AS STRING))) FROM UNNEST(event_params) p WHERE p.key='" + key + "')"
    return f"""WITH events AS (
      SELECT event_date, platform, stream_id, app_info.version AS app_version, event_name,
        {param('event_label')} AS event_label,
        EXISTS(SELECT 1 FROM UNNEST(event_params) p WHERE p.key='event_label') AS event_label_parameter_present,
        {param('screen_view')} AS screen_view,
        {param('event_category')} AS event_category,
        {param('value')} AS value,
        EXISTS(SELECT 1 FROM UNNEST(event_params) p WHERE p.key='value') AS value_parameter_present,
        ARRAY_LENGTH(event_params) - (SELECT COUNT(DISTINCT key) FROM UNNEST(event_params)) AS duplicate_param_keys
      FROM `{project}.{dataset}.events_*`
      WHERE {suffix_filter}
        AND (event_name IN ('DA1','DA2') OR UPPER(event_name) IN ('CAMPUS','BUSINESS','USER')
          OR (platform = 'ANDROID' AND (event_name IN ('DA1_debug','DA2_debug') OR UPPER(event_name) IN ('CAMPUS_DEBUG','BUSINESS_DEBUG','USER_DEBUG')))
          OR EXISTS(SELECT 1 FROM UNNEST(event_params) p WHERE p.key='event_label'))
    )
    SELECT *, COUNT(*) AS event_count FROM events GROUP BY ALL"""


def fetch(project, dataset, start, end, max_bytes=5 * 1024**3, include_intraday=False):
    from google.cloud import bigquery
    client = bigquery.Client(project=project)
    # Missing daily tables must never be reported as zero traffic / success.
    expected = set()
    cursor = date.fromisoformat(start)
    while cursor <= date.fromisoformat(end):
        expected.add('events_' + cursor.strftime('%Y%m%d'))
        cursor += timedelta(days=1)
    tables = {x.table_id for x in client.list_tables(f'{project}.{dataset}')}
    today_suffix = datetime.now(timezone(timedelta(hours=9))).strftime('%Y%m%d')
    intraday_date = None
    if include_intraday and end.replace('-', '') == today_suffix and 'events_' + today_suffix not in tables and 'events_intraday_' + today_suffix in tables:
        intraday_date = today_suffix
        expected.discard('events_' + today_suffix)
    missing = sorted(expected - tables)
    config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('start_suffix', 'STRING', start.replace('-', '')),
                          bigquery.ScalarQueryParameter('end_suffix', 'STRING', end.replace('-', ''))],
        maximum_bytes_billed=max_bytes, use_legacy_sql=False)
    job = client.query(build_query(project, dataset, intraday_date), job_config=config)
    observations = []
    for row in job.result(timeout=600):
        observations.append(dict(row))
        if len(observations) > 200000:
            job.cancel()
            raise RuntimeError('Observation cardinality exceeded safe audit limit')
    return dict(rows=observations, missing_daily_tables=missing, complete=not missing,
                job_id=job.job_id, bytes_processed=job.total_bytes_processed, intraday_date=intraday_date)
