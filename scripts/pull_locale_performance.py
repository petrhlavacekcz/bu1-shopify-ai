#!/usr/bin/env python3
"""
GA4 + GSC Locale Performance Audit
Pulls sessions, engagement, revenue by country/locale from GA4
and impressions/clicks/CTR/position from GSC for bu1.cz + bu1sport.com
"""

import json
import os
import sys
from datetime import datetime, timedelta

# ── GA4 ──────────────────────────────────────────────────────────────────────

def get_ga4_service():
    from google.oauth2 import service_account
    from google.analytics.data_v1beta import BetaAnalyticsDataClient

    # Build service account credentials from .mcp.json private key
    mcp_path = os.path.join(os.path.dirname(__file__), '..', '.mcp.json')
    with open(mcp_path) as f:
        mcp = json.load(f)

    ga_env = mcp['mcpServers']['google-analytics-mcp']['env']
    private_key = ga_env['GOOGLE_PRIVATE_KEY'].replace('\\n', '\n')

    creds = service_account.Credentials.from_service_account_info({
        "type": "service_account",
        "project_id": "geminiapi-petr",
        "private_key": private_key,
        "client_email": ga_env['GOOGLE_CLIENT_EMAIL'],
        "token_uri": "https://oauth2.googleapis.com/token",
    }, scopes=["https://www.googleapis.com/auth/analytics.readonly"])

    return BetaAnalyticsDataClient(credentials=creds), ga_env['GA_PROPERTY_ID']


def pull_ga4_locale_data(days=90):
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Dimension, Metric, OrderBy
    )

    client, property_id = get_ga4_service()
    end = datetime.today()
    start = end - timedelta(days=days)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(
            start_date=start.strftime('%Y-%m-%d'),
            end_date=end.strftime('%Y-%m-%d'),
        )],
        dimensions=[
            Dimension(name="country"),
            Dimension(name="sessionDefaultChannelGroup"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="conversions"),
            Metric(name="totalRevenue"),
        ],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=200,
    )

    response = client.run_report(request)
    rows = []
    for row in response.rows:
        rows.append({
            'country': row.dimension_values[0].value,
            'channel': row.dimension_values[1].value,
            'sessions': int(row.metric_values[0].value or 0),
            'engaged_sessions': int(row.metric_values[1].value or 0),
            'engagement_rate': float(row.metric_values[2].value or 0),
            'avg_session_duration': float(row.metric_values[3].value or 0),
            'conversions': float(row.metric_values[4].value or 0),
            'revenue': float(row.metric_values[5].value or 0),
        })
    return rows


def pull_ga4_landing_pages(days=90):
    """Top landing pages by locale prefix"""
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Dimension, Metric, OrderBy
    )

    client, property_id = get_ga4_service()
    end = datetime.today()
    start = end - timedelta(days=days)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(
            start_date=start.strftime('%Y-%m-%d'),
            end_date=end.strftime('%Y-%m-%d'),
        )],
        dimensions=[
            Dimension(name="landingPagePlusQueryString"),
            Dimension(name="country"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="conversions"),
            Metric(name="totalRevenue"),
            Metric(name="bounceRate"),
        ],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=100,
    )

    response = client.run_report(request)
    rows = []
    for row in response.rows:
        rows.append({
            'page': row.dimension_values[0].value,
            'country': row.dimension_values[1].value,
            'sessions': int(row.metric_values[0].value or 0),
            'conversions': float(row.metric_values[1].value or 0),
            'revenue': float(row.metric_values[2].value or 0),
            'bounce_rate': float(row.metric_values[3].value or 0),
        })
    return rows


# ── GSC ──────────────────────────────────────────────────────────────────────

def get_gsc_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    with open('/Users/petrhlavacek/bu1-oauth.json') as f:
        oauth = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=oauth['refresh_token'],
        client_id=oauth['client_id'],
        client_secret=oauth['client_secret'],
        token_uri='https://oauth2.googleapis.com/token',
    )
    return build('searchconsole', 'v1', credentials=creds)


def pull_gsc_data(service, site_url, days=90):
    end = datetime.today()
    start = end - timedelta(days=days)

    body = {
        'startDate': start.strftime('%Y-%m-%d'),
        'endDate': end.strftime('%Y-%m-%d'),
        'dimensions': ['query', 'country'],
        'rowLimit': 500,
        'startRow': 0,
    }

    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = []
    for row in response.get('rows', []):
        rows.append({
            'site': site_url,
            'query': row['keys'][0],
            'country': row['keys'][1],
            'clicks': row.get('clicks', 0),
            'impressions': row.get('impressions', 0),
            'ctr': row.get('ctr', 0),
            'position': row.get('position', 0),
        })
    return rows


def pull_gsc_pages(service, site_url, days=90):
    end = datetime.today()
    start = end - timedelta(days=days)

    body = {
        'startDate': start.strftime('%Y-%m-%d'),
        'endDate': end.strftime('%Y-%m-%d'),
        'dimensions': ['page', 'country'],
        'rowLimit': 500,
    }

    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = []
    for row in response.get('rows', []):
        rows.append({
            'site': site_url,
            'page': row['keys'][0],
            'country': row['keys'][1],
            'clicks': row.get('clicks', 0),
            'impressions': row.get('impressions', 0),
            'ctr': row.get('ctr', 0),
            'position': row.get('position', 0),
        })
    return rows


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=== Pulling GA4 locale data (90 days)...")
    try:
        ga4_locale = pull_ga4_locale_data(90)
        print(f"  GA4 locale rows: {len(ga4_locale)}")
    except Exception as e:
        print(f"  GA4 locale ERROR: {e}")
        ga4_locale = []

    print("=== Pulling GA4 landing pages (90 days)...")
    try:
        ga4_pages = pull_ga4_landing_pages(90)
        print(f"  GA4 pages rows: {len(ga4_pages)}")
    except Exception as e:
        print(f"  GA4 pages ERROR: {e}")
        ga4_pages = []

    print("=== Pulling GSC data...")
    gsc_cz = []
    gsc_com = []
    gsc_pages_cz = []
    gsc_pages_com = []
    try:
        svc = get_gsc_service()
        gsc_cz = pull_gsc_data(svc, 'sc-domain:bu1.cz', 90)
        print(f"  GSC bu1.cz queries: {len(gsc_cz)}")
        gsc_com = pull_gsc_data(svc, 'sc-domain:bu1sport.com', 90)
        print(f"  GSC bu1sport.com queries: {len(gsc_com)}")
        gsc_pages_cz = pull_gsc_pages(svc, 'sc-domain:bu1.cz', 90)
        print(f"  GSC bu1.cz pages: {len(gsc_pages_cz)}")
        gsc_pages_com = pull_gsc_pages(svc, 'sc-domain:bu1sport.com', 90)
        print(f"  GSC bu1sport.com pages: {len(gsc_pages_com)}")
    except Exception as e:
        print(f"  GSC ERROR: {e}")

    # Save raw data
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', '_raw')
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, 'ga4_locale.json'), 'w') as f:
        json.dump(ga4_locale, f, indent=2)
    with open(os.path.join(out_dir, 'ga4_pages.json'), 'w') as f:
        json.dump(ga4_pages, f, indent=2)
    with open(os.path.join(out_dir, 'gsc_cz_queries.json'), 'w') as f:
        json.dump(gsc_cz, f, indent=2)
    with open(os.path.join(out_dir, 'gsc_com_queries.json'), 'w') as f:
        json.dump(gsc_com, f, indent=2)
    with open(os.path.join(out_dir, 'gsc_cz_pages.json'), 'w') as f:
        json.dump(gsc_pages_cz, f, indent=2)
    with open(os.path.join(out_dir, 'gsc_com_pages.json'), 'w') as f:
        json.dump(gsc_pages_com, f, indent=2)

    print(f"\nRaw data saved to reports/_raw/")
    print(f"GA4 locale: {len(ga4_locale)} rows | GA4 pages: {len(ga4_pages)} rows")
    print(f"GSC bu1.cz: {len(gsc_cz)} queries, {len(gsc_pages_cz)} pages")
    print(f"GSC bu1sport.com: {len(gsc_com)} queries, {len(gsc_pages_com)} pages")
