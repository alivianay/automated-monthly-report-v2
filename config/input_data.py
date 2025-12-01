from core.bigquery_utils import get_total_customer_netmonk, get_total_mau, get_order_progress, get_category_order, get_total_devices
from core.ga_utils import get_all_data_netmonk

# url dashboard
LOOKER_DASHBOARD_URL = 'https://lookerstudio.google.com/reporting/08a17056-be12-41b2-9ee2-dfacf316f548'

# slide template dan folder drive
TEMPLATE_PRESENTATION_ID = 'INPUT YOUR ID' #masukkan TEMPLATE_PRESENTATION_ID
DESTINATION_FOLDER_ID = 'INPUT YOUR ID' #masukkan DESTINATION_FOLDER_ID
SCREENSHOT_FOLDER_ID = 'INPUT YOUR ID' #masukkan SCREENSHOT_FOLDER_ID


# slide title & placeholder
FILE_NAME = 'Monthly Report - November 2025'

get_data_customer = get_total_customer_netmonk()
get_data_mau = get_total_mau()
get_data_orders = get_order_progress()
get_order_category = get_category_order()
get_data_engagement = get_all_data_netmonk()
get_data_devices = get_total_devices()


TEXT_REPLACEMENT = {
    '{bulan_monthly_report}': 'November 2025',

    # total customer Netmonk, Netmonk Prime, Netmonk Hi
    '{total_customer_netmonk}': get_data_customer["total_customer_netmonk"],
    '{persentase_updown_customer_netmonk}': get_data_customer["persentase_updown_netmonk"],
    '{total_customer_prime}': get_data_customer["total_customer_prime"],
    '{persentase_updown_prime}': get_data_customer["persentase_updown_prime"],
    '{total_customer_hi}': get_data_customer["total_customer_hi"],
    '{persentase_updown_hi}': get_data_customer["persentase_updown_hi"],

    # total MAU Netmonk, Netmonk Prime, Netmonk Hi
    '{mau_netmonk}': get_data_mau["total_mau_netmonk"],
    '{mau_percentage_netmonk}': get_data_mau["mau_percentage_netmonk"],
    '{growth_mau_netmonk}': get_data_mau ["growth_mau_netmonk"],
    '{mau_prime}': get_data_mau["total_mau_prime"],
    '{mau_percentage_prime}': get_data_mau["mau_percentage_prime"],
    '{growth_mau_prime}': get_data_mau ["growth_mau_prime"],
    '{mau_hi}': get_data_mau["total_mau_hi"],
    '{mau_percentage_hi}': get_data_mau["mau_percentage_hi"],
    '{growth_mau_hi}': get_data_mau ["growth_mau_hi"],

    # total order netmonk
    '{total_order}': get_data_orders["total_orders"],
    '{growth_total_order}': get_data_orders["growth_orders"],
    '{total_completed_order}': get_data_orders["total_completed_orders"],
    '{percentage_total_completed_order}': get_data_orders["completed_orders_percentage"],
    '{total_onprogress_order}': get_data_orders["total_on_progress_orders"],
    '{percentage_total_onprogress_order}': get_data_orders["on_progress_orders_percentage"],

    # total order by category
    '{remaining_order_prime}': get_order_category["remaining_order_prime"],
    '{remaining_order_hi}': get_order_category["remaining_order_hi"],
    '{top_remaining_order_regional}': get_order_category["remaining_order_regional"],
    '{total_remaining_order_regional}': get_order_category["total_remaining_order_regional"],
    '{total_order_BA_document}': get_order_category["contract_document"],

    # Netmonk Portal
    '{total_visitor_website}': get_data_engagement["total_visitors_website"],
    '{growth_visitor_website}': get_data_engagement["growth_total_visitors_website"],
    '{summary_metrics_website}': get_data_engagement["summary_website"],
    
    # Netmonk Prime
    '{total_visitor_prime}': get_data_engagement["total_visitors_prime"],
    '{growth_visitor_prime}': get_data_engagement["growth_total_visitors_prime"],
    '{page_views_prime}': get_data_engagement["page_views_prime"],
    '{growth_page_views_prime}': get_data_engagement["growth_page_views_prime"],
    '{growth_engagement_rate_prime}': get_data_engagement["growth_engagement_rate_prime"],
    '{total_devices_prime}': get_data_devices["total_devices_prime"],
    '{growth_devices_prime}': get_data_devices["growth_devices_prime"],

    # Netmonk HI
    '{summary_metrics_hi}': get_data_engagement["summary_hi"],
    '{total_visitor_hi}': get_data_engagement["total_visitors_hi"],
    '{growth_visitor_hi}': get_data_engagement["growth_total_visitors_hi"],
    '{page_views_hi}': get_data_engagement["page_views_hi"],
    '{growth_page_views_hi}': get_data_engagement["growth_page_views_hi"],
    '{growth_engagement_rate_hi}': get_data_engagement["growth_engagement_rate_hi"],
    '{growth_engagement_time_hi}': get_data_engagement["growth_avg_engagement_time_hi"],
    '{total_devices_hi}': get_data_devices["total_devices_hi"],
    '{growth_devices_hi}': get_data_devices["growth_devices_hi"],
}

ELEMENT_TO_CAPTURE = [
    # # slide 5 - fixed elements
    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(7)",
    #     "slide_index": 4,
    #     "title" : "Graphic Monitoring Active Users",
    #     "x": 70,
    #     "y": 50,
    #     "width": 400,
    #     "height": 250
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(8) > ng2-canvas-component",
    #     "slide_index": 4,
    #     "title" : "Total Customers",
    #     "x": 500,
    #     "y": 30,
    #     "width": 120,
    #     "height": 150
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(9)",
    #     "slide_index": 4,
    #     "title" : "Active Users",
    #     "x": 500,
    #     "y": 90,
    #     "width": 120,
    #     "height": 150
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(10) > ng2-canvas-component",
    #     "slide_index": 4,
    #     "title" : "MAU Percentage",
    #     "x": 500,
    #     "y": 150,
    #     "width": 120,
    #     "height": 150
    # },

    # # slide 6 - fixed elements
    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(16)",
    #         "slide_index": 5,
    #         "title" : "Key metrics",
    #         "x": 50,
    #         "y": 35,
    #         "width": 80,
    #         "height": 100
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(11)",
    #         "slide_index": 5,
    #         "title" : "Key metrics - Total Pageviews",
    #         "x": 80,
    #         "y": 80,
    #         "width": 100,
    #         "height": 100
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(12)",
    #         "slide_index": 5,
    #         "title" : "Key metrics - Total Visitors",
    #         "x": 195,
    #         "y": 80,
    #         "width": 100,
    #         "height": 100
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(13)",
    #         "slide_index": 5,
    #         "title" : "Key metrics - Avg Engagement Time",
    #         "x": 310,
    #         "y": 80,
    #         "width": 100,
    #         "height": 100
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(14)",
    #         "slide_index": 5,
    #         "title" : "Key metrics - Engagement Rate",
    #         "x": 425,
    #         "y": 80,
    #         "width": 100,
    #         "height": 100
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(15)",
    #         "slide_index": 5,
    #         "title" : "Key metrics - Bounced Rate",
    #         "x": 540,
    #         "y": 80,
    #         "width": 100,
    #         "height": 100
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(17)",
    #         "slide_index": 5,
    #         "title" : "Top Visited Pages",
    #         "x": 150,
    #         "y": 100,
    #         "width": 450,
    #         "height": 300
    #     },

    # # # slide 7 - fixed elements
    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(18)",
    #     "slide_index": 6,
    #     "title" : "NCX Order Per Hari",
    #     "x": 150,
    #     "y": 8,
    #     "width": 300,
    #     "height": 250
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(19)",
    #     "slide_index": 6,
    #     "title" : "Total Order",
    #     "x": 450,
    #     "y": 8,
    #     "width": 120,
    #     "height": 150
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(20)",
    #     "slide_index": 6,
    #     "title" : "PIE Chart Total Order",
    #     "x": 450,
    #     "y": 90,
    #     "width": 125,
    #     "height": 125
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(21)",
    #     "slide_index": 6,
    #     "title" : "Order vs Closing",
    #     "x": 150,
    #     "y": 163,
    #     "width": 200,
    #     "height": 175
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(22)",
    #     "slide_index": 6,
    #     "title" : "Order by Status Fulfillment",
    #     "x": 360,
    #     "y": 165,
    #     "width": 200,
    #     "height": 175
    # },

    # # # slide 8
    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(23)",
    #     "slide_index": 7,
    #     "title" : "Remaining Order Product",
    #     "x": 50,
    #     "y": 70,
    #     "width": 300,
    #     "height": 200
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(24)",
    #     "slide_index": 7,
    #     "title" : "Remaining Order Region",
    #     "x": 365,
    #     "y": 70,
    #     "width": 300,
    #     "height": 200
    # },  

    # #slide 10 - fixed elements
    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(11)",
    #         "slide_index": 9,
    #         "title" : "Key metrics",
    #         "x": 50,
    #         "y": 50,
    #         "width": 80,
    #         "height": 100,
    #         "tab": "text=Netmonk Prime",
    #         "wait_for": "text=Key Metrics"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(6)",
    #         "slide_index": 9,
    #         "title" : "Key metrics - Total Pageviews",
    #         "x": 80,
    #         "y": 100,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk Prime",
    #         "wait_for": "text=Total Pageview"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(7)",
    #         "slide_index": 9,
    #         "title" : "Key metrics - Total Visitors",
    #         "x": 200,
    #         "y": 100,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk Prime",
    #         "wait_for": "text=Total Visitors"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(8)",
    #         "slide_index": 9,
    #         "title" : "Key metrics - Avg Engagement Rate",
    #         "x": 320,
    #         "y": 100,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk Prime",
    #         "wait_for": "text=Avg Engagement Rate"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(9)",
    #         "slide_index": 9,
    #         "title" : "Key metrics - Engagement Rate",
    #         "x": 440,
    #         "y": 100,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk Prime",
    #         "wait_for": "text=Engagement Rate"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(10)",
    #         "slide_index": 9,
    #         "title" : "Key metrics - Bounce Rate",
    #         "x": 560,
    #         "y": 100,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk Prime",
    #         "wait_for": "text=Bounce Rate"
    #     },
    
    # slide 11 - fixed elements
    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(12)",
        "slide_index": 10,
        "title": "Network Monitoring Prime",
        "x": 50,
        "y": 70,
        "width": 250,
        "height": 150,
        "tab": "text=Netmonk Prime",
        "wait_for": "text=total_customer"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(14)",
        "slide_index": 10,
        "title": "Total Customer Prime",
        "x": 40,
        "y": 170,
        "width": 120,
        "height": 150,
        "tab": "text=Netmonk Prime",
        "wait_for": "text=Total Customer"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(20)",
        "slide_index": 10,
        "title": "MAU Prime",
        "x": 40,
        "y": 220,
        "width": 120,
        "height": 150,
        "tab": "text=Netmonk Prime",
        "wait_for": "text=MAU"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(19)",
        "slide_index": 10,
        "title": "Total Devices Prime",
        "x": 40,
        "y": 270,
        "width": 120,
        "height": 150,
        "tab": "text=Netmonk Prime",
        "wait_for": "text=Total Devices"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(13)",
        "slide_index": 10,
        "title": "MAU Percentage Prime",
        "x": 160,
        "y": 190,
        "width": 150,
        "height": 250,
        "tab": "text=Netmonk Prime",
        "wait_for": "text=MAU Percentage"
    },

    # # slide 12 - fixed elements
    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(17)",
    #     "slide_index": 11,
    #     "title" : "Comparison of Network Features",
    #     "x": 50,
    #     "y": 10,
    #     "width": 325,
    #     "height": 250,
    #     "tab": "text=Netmonk Prime",
    #     "wait_for": "text=Comparison of Network Feature"
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(18)",
    #     "slide_index": 11,
    #     "title" : "Comparison of Server Features",
    #     "x": 50,
    #     "y": 125,
    #     "width": 325,
    #     "height": 250,
    #     "tab": "text=Netmonk Prime",
    #     "wait_for": "text=Comparison of Server Feature"
    # },

    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(19)",
    #     "slide_index": 11,
    #     "title" : "Comparison of Network Features",
    #     "x": 50,
    #     "y": 235,
    #     "width": 325,
    #     "height": 250,
    #     "tab": "text=Netmonk Prime",
    #     "wait_for": "text=Comparison of Network Feature"
    # },

    # # slide 14 - fixed elements
    # {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(11)",
    #         "slide_index": 13,
    #         "title" : "Key metrics HI",
    #         "x": 50,
    #         "y": 60,
    #         "width": 80,
    #         "height": 100,
    #         "tab": "text=Netmonk HI",
    #         "wait_for": "text=Key Metrics"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(6)",
    #         "slide_index": 13,
    #         "title" : "Key metrics Hi - Total Pageviews",
    #         "x": 80,
    #         "y": 105,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk HI",
    #         "wait_for": "text=Total Page Views"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(7)",
    #         "slide_index": 13,
    #         "title" : "Key metrics Hi- Total Visitors",
    #         "x": 200,
    #         "y": 105,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk HI",
    #         "wait_for": "text=Total Visitors"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(8)",
    #         "slide_index": 13,
    #         "title" : "Key metrics Hi - Avg Engagement Time",
    #         "x": 320,
    #         "y": 105,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk HI",
    #         "wait_for": "text=Avg Engagement Time"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(9)",
    #         "slide_index": 13,
    #         "title" : "Key metrics Hi - Engagement Rate",
    #         "x": 440,
    #         "y": 105,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk HI",
    #         "wait_for": "text=Engagement Rate"
    #     },

    #     {
    #         "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(10)",
    #         "slide_index": 13,
    #         "title" : "Key metrics Hi - Bounce Rate",
    #         "x": 560,
    #         "y": 105,
    #         "width": 100,
    #         "height": 100,
    #         "tab": "text=Netmonk HI",
    #         "wait_for": "text=Bounced Rate"
    #     },

    # #slide 15 - fixed elements
    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(13)",
        "slide_index": 14,
        "title" : "Customer Monitoring HI",
        "x": 50,
        "y": 70,
        "width": 250,
        "height": 150,
        "tab": "text=Netmonk HI",
        "wait_for": "text=total_customer"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(15)",
        "slide_index": 14,
        "title" : "Total Customer HI",
        "x": 40,
        "y": 170,
        "width": 120,
        "height": 150,
        "tab": "text=Netmonk HI",
        "wait_for": "text=Total Customer"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(16)",
        "slide_index": 14,
        "title" : "MAU HI",
        "x": 40,
        "y": 220,
        "width": 120,
        "height": 150,
        "tab": "text=Netmonk HI",
        "wait_for": "text=MAU"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(18)",
        "slide_index": 14,
        "title": "Total Devices HI",
        "x": 40,
        "y": 270,
        "width": 120,
        "height": 150,
        "tab": "text=Netmonk HI",
        "wait_for": "text=Total Devices"
    },

    {
        "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(14)",
        "slide_index": 14,
        "title" : "MAU Percentage Hi",
        "x": 160,
        "y": 190,
        "width": 150,
        "height": 250,
        "tab": "text=Netmonk HI",
        "wait_for": "text=MAU Percentage"
    }

    # ## slide 16 - fixed elements
    # {
    #     "selector": "#body > div.lego-reporting-view.activity-view.no-licensed.new-resizer > div > ng2-reporting-plate > plate > div > div > div > div:nth-child(1) > div > div > div > div.pancake-container > div:nth-child(2) > canvas-pancake-adapter > canvas-layout > div > div > div.mainBlockHolder > div > div > div > ng2-report > ng2-canvas-container > div > div:nth-child(12)",
    #     "slide_index": 15,
    #     "title" : "Netmonk Hi Favorite Features",
    #     "x": 50,
    #     "y": -40,
    #     "width": 600,
    #     "height": 500,
    #     "tab": "text=Netmonk HI",
    #     "wait_for": "text=Favorite Features"
    # }
]