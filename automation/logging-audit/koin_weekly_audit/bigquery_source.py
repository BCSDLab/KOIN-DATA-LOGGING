import re
from datetime import date, timedelta


def build_query(project, dataset):
    if not re.fullmatch(r'[a-z][a-z0-9-]+', project) or not re.fullmatch(r'[A-Za-z0-9_]+', dataset):
        raise ValueError('Invalid BigQuery identifier')
    def param(key):
        return "(SELECT ANY_VALUE(COALESCE(p.value.string_value, CAST(p.value.int_value AS STRING), CAST(p.value.double_value AS STRING), CAST(p.value.float_value AS STRING))) FROM UNNEST(event_params) p WHERE p.key='" + key + "')"
    return f"""WITH events AS (
      SELECT event_date, platform, stream_id, app_info.version AS app_version, event_name,
        {param('event_label')} AS event_label,
        {param('screen_view')} AS screen_view,
        {param('event_category')} AS event_category,
        {param('value')} AS value,
        ARRAY_LENGTH(event_params) - (SELECT COUNT(DISTINCT key) FROM UNNEST(event_params)) AS duplicate_param_keys
      FROM `{project}.{dataset}.events_*`
      WHERE _TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix
        AND REGEXP_CONTAINS(_TABLE_SUFFIX, r'^[0-9]{{8}}$')
        AND event_name IN ('DA1','DA2')
    )
    SELECT *, COUNT(*) AS event_count FROM events GROUP BY ALL"""


def fetch(project, dataset, start, end, max_bytes=5 * 1024**3):
    from google.cloud import bigquery
    client = bigquery.Client(project=project)
    # Missing daily tables must never be reported as zero traffic / success.
    expected = set()
    cursor = date.fromisoformat(start)
    while cursor <= date.fromisoformat(end):
        expected.add('events_' + cursor.strftime('%Y%m%d'))
        cursor += timedelta(days=1)
    tables = {x.table_id for x in client.list_tables(f'{project}.{dataset}')}
    missing = sorted(expected - tables)
    config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter('start_suffix', 'STRING', start.replace('-', '')),
                          bigquery.ScalarQueryParameter('end_suffix', 'STRING', end.replace('-', ''))],
        maximum_bytes_billed=max_bytes, use_legacy_sql=False)
    job = client.query(build_query(project, dataset), job_config=config)
    observations = []
    for row in job.result(timeout=600):
        observations.append(dict(row))
        if len(observations) > 200000:
            job.cancel()
            raise RuntimeError('Observation cardinality exceeded safe audit limit')
    return dict(rows=observations, missing_daily_tables=missing, complete=not missing,
                job_id=job.job_id, bytes_processed=job.total_bytes_processed)
