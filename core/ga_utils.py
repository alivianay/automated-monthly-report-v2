import os
import datetime
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest

# ==========================================================
# AUTHENTICATION
# ==========================================================
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
OAUTH_CLIENT_SECRET_FILES = ["credential_google.json", "credentials_google.json"]
TOKEN_FILE = "token_ga4.pkl"

# Ganti dengan GA4 Property ID masing-masing produk
PROPERTY_NETMONK_WEBSITE = "341788918"   # contoh
PROPERTY_NETMONK_PRIME = "347995250"
PROPERTY_NETMONK_HI = "326779667"


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_secret_file = next(
                (path for path in OAUTH_CLIENT_SECRET_FILES if os.path.exists(path)),
                None,
            )
            if not client_secret_file:
                raise FileNotFoundError(
                    "Tidak menemukan file kredensial Google. "
                    "Tambahkan salah satu file berikut ke folder project: "
                    "credential_google.json atau credentials_google.json."
                )
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds


# ==========================================================
# GA4 METRICS HELPER
# ==========================================================
def get_metrics_for_netmonk(client, start_date, end_date, property_id):
    """Ambil metrik utama GA4 untuk periode tertentu"""
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[],
        metrics=[
            Metric(name="totalUsers"),
            Metric(name="screenPageViews"),
            Metric(name="engagementRate"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
        ],
        date_ranges=[DateRange(start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d"))],
    )
    response = client.run_report(request)

    metrics = {
        "totalUsers": float(response.rows[0].metric_values[0].value),
        "screenPageViews": float(response.rows[0].metric_values[1].value),
        "engagementRate": float(response.rows[0].metric_values[2].value),
        "bounceRate": float(response.rows[0].metric_values[3].value),
        "avgEngagementTime": float(response.rows[0].metric_values[4].value),
    }
    return metrics


def compare_metric_for_netmonk(current, previous):
    """Hitung growth (%) dibanding periode sebelumnya"""
    if previous == 0:
        return "N/A"
    growth = ((current - previous) / previous) * 100
    
    if growth > 0:
        return f"meningkat sebanyak {growth:.2f}%"
    elif growth < 0:
        return f"menurun sebanyak {growth:.2f}%"
    else:
        return "tidak berubah"


# ==========================================================
# MAIN WRAPPER PER PRODUK
# ==========================================================
def get_summary_metrics_netmonk(property_id, suffix):
    """Return variabel terpisah (flat dict) siap dipakai di TEXT_REPLACEMENT"""
    creds = get_credentials()
    client = BetaAnalyticsDataClient(credentials=creds)

    today = datetime.date.today()
    first_day_this_month = today.replace(day=1)

    # Bulan lalu
    last_month_end = first_day_this_month - datetime.timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # 2 bulan lalu
    two_months_ago_end = last_month_start - datetime.timedelta(days=1)
    two_months_ago_start = two_months_ago_end.replace(day=1)

    # 🔹 Ambil metriks
    metrics_last_month = get_metrics_for_netmonk(client, last_month_start, last_month_end, property_id)
    metrics_two_months_ago = get_metrics_for_netmonk(client, two_months_ago_start, two_months_ago_end, property_id)

    # 🔹 Variabel langsung
    month_total = last_month_start.strftime("%B %Y")

    total_users = f"{metrics_last_month['totalUsers']:,.0f}".replace(",", ".")
    growth_total_users = compare_metric_for_netmonk(metrics_last_month["totalUsers"], metrics_two_months_ago["totalUsers"])

    page_views = f"{metrics_last_month['screenPageViews']:,.0f}".replace(",", ".")
    growth_page_views = compare_metric_for_netmonk(metrics_last_month["screenPageViews"], metrics_two_months_ago["screenPageViews"])

    engagement_rate = f"{metrics_last_month['engagementRate']:.2f}".replace(",", ".")
    growth_engagement_rate = compare_metric_for_netmonk(metrics_last_month["engagementRate"], metrics_two_months_ago["engagementRate"])

    bounce_rate = f"{metrics_last_month['bounceRate']:.2f}".replace(",", ".")
    growth_bounce_rate = compare_metric_for_netmonk(metrics_last_month["bounceRate"], metrics_two_months_ago["bounceRate"])

    avg_engagement_time = f"{metrics_last_month['avgEngagementTime']:.2f}".replace(",", ".")
    growth_avg_engagement_time = compare_metric_for_netmonk(metrics_last_month["avgEngagementTime"], metrics_two_months_ago["avgEngagementTime"])

    # 🔹 Tentukan summary peningkatan
    growth_metrics = []
    if metrics_last_month["totalUsers"] > metrics_two_months_ago["totalUsers"]:
        growth_metrics.append("total visitor")
    if metrics_last_month["screenPageViews"] > metrics_two_months_ago["screenPageViews"]:
        growth_metrics.append("page view")
    if metrics_last_month["engagementRate"] > metrics_two_months_ago["engagementRate"]:
        growth_metrics.append("engagement rate")
    if metrics_last_month["avgEngagementTime"] > metrics_two_months_ago["avgEngagementTime"]:
        growth_metrics.append("engagement time")
    if metrics_last_month["bounceRate"] > metrics_two_months_ago["bounceRate"]:
        growth_metrics.append("bounce rate")

    if growth_metrics:
        summary = ", ".join(growth_metrics[:-1]) + f" dan {growth_metrics[-1]}" if len(growth_metrics) > 1 else growth_metrics[0]
        summary_text = f"{summary} mengalami peningkatan dari bulan lalu."
    else:
        summary_text = "Tidak ada metrik utama yang mengalami peningkatan dari bulan lalu."

    # 🔹 Simpan dalam dictionary data_engagement_netmonk
    data_engagement_netmonk = {
        f"month_{suffix}": month_total,
        f"total_visitors_{suffix}": total_users,
        f"growth_total_visitors_{suffix}": growth_total_users,
        f"page_views_{suffix}": page_views,
        f"growth_page_views_{suffix}": growth_page_views,
        f"engagement_rate_{suffix}": engagement_rate,
        f"growth_engagement_rate_{suffix}": growth_engagement_rate,
        f"bounce_rate_{suffix}": bounce_rate,
        f"growth_bounce_rate_{suffix}": growth_bounce_rate,
        f"avg_engagement_time_{suffix}": avg_engagement_time,
        f"growth_avg_engagement_time_{suffix}": growth_avg_engagement_time,
        f"summary_{suffix}": summary_text,
    }

    return data_engagement_netmonk

# ==========================================================
# GET ALL DATA
# ==========================================================
def get_all_data_netmonk():
    data_netmonk_website = get_summary_metrics_netmonk(PROPERTY_NETMONK_WEBSITE, "website")
    data_netmonk_prime = get_summary_metrics_netmonk(PROPERTY_NETMONK_PRIME, "prime")
    data_netmonk_hi = get_summary_metrics_netmonk(PROPERTY_NETMONK_HI, "hi")

    return {**data_netmonk_website, **data_netmonk_prime, **data_netmonk_hi}