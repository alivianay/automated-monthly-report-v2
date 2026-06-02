from google.cloud import bigquery

def get_total_customer_netmonk():
    client = bigquery.Client.from_service_account_json("service_account.json")

    QUERY = f"""
      WITH monthly_data AS (
        SELECT
          product,
          DATE_TRUNC(month, MONTH) AS month,
          SUM(total_customer) AS total_customer
        FROM `L4_datamart.netmonk_mau`
        WHERE product IN ('Netmonk', 'Netmonk Prime', 'Netmonk HI')
          AND month IN (
            DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH), MONTH),
            DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
          )
        GROUP BY product, month
      ),
      calc AS (
        SELECT
          product,
          month,
          total_customer,
          ROUND(
            (total_customer - LAG(total_customer) OVER (PARTITION BY product ORDER BY month))
            / LAG(total_customer) OVER (PARTITION BY product ORDER BY month) * 100,
            2
          ) AS persentase
        FROM monthly_data
      )
      SELECT
        product,
        REPLACE(FORMAT("%'d", total_customer), ",", ".") AS total_customer_formatted,
        CASE 
          WHEN persentase > 0 THEN CONCAT('meningkat sebanyak ', CAST(persentase AS STRING), '%')
          WHEN persentase < 0 THEN CONCAT('menurun sebanyak ', CAST(ABS(persentase) AS STRING), '%')
          ELSE 'Tetap 0%'
        END AS persentase_updown
      FROM calc
      WHERE month = DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
      ORDER BY product
    """

    query_job = client.query(QUERY)
    rows = list(query_job.result())

    print(f"🔍 get_total_customer_netmonk: Query returned {len(rows)} rows")  # ADD THIS
    for row in rows:
        print(f"  Row: {row}")

    data_customer = {}
    for row in rows:
        if row.product == "Netmonk":
            data_customer["total_customer_netmonk"] = row.total_customer_formatted
            data_customer["persentase_updown_netmonk"] = row.persentase_updown
        elif row.product == "Netmonk Prime":
            data_customer["total_customer_prime"] = row.total_customer_formatted
            data_customer["persentase_updown_prime"] = row.persentase_updown
        elif row.product == "Netmonk HI":
            data_customer["total_customer_hi"] = row.total_customer_formatted
            data_customer["persentase_updown_hi"] = row.persentase_updown
    
    print(f"📊 Final data_customer: {data_customer}")
    return data_customer

def get_total_mau():
    client = bigquery.Client.from_service_account_json("service_account.json")

    QUERY = f"""
WITH monthly_data AS (
  SELECT
    product,
    DATE_TRUNC(month, MONTH) AS month,
    SUM(mau) AS total_mau,
    AVG(ratio) AS mau_percentage
  FROM `L4_datamart.netmonk_mau`
  WHERE product IN ('Netmonk', 'Netmonk Prime', 'Netmonk HI')
    AND month IN (
      DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH), MONTH),
      DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
    )
  GROUP BY product, month
),
calc AS (
  SELECT
    product,
    month,
    total_mau,
    mau_percentage,
    ROUND(
      (total_mau - LAG(total_mau) OVER (PARTITION BY product ORDER BY month)) 
      / LAG(total_mau) OVER (PARTITION BY product ORDER BY month) * 100,
      2
    ) AS persentase
  FROM monthly_data
)
SELECT
  product,
  total_mau,
  mau_percentage,
  REPLACE(FORMAT("%'d", total_mau), ",", ".") AS total_mau_formatted,
  FORMAT("%.2f%%", mau_percentage * 100) AS mau_percentage_formatted,
  CASE 
    WHEN persentase > 0 THEN CONCAT('meningkat sebanyak ', CAST(persentase AS STRING), '%')
    WHEN persentase < 0 THEN CONCAT('menurun sebanyak ', CAST(ABS(persentase) AS STRING), '%')
    ELSE 'Tetap 0%'
  END AS growth_mau
FROM calc
WHERE month = DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
    """

    query_job = client.query(QUERY)
    rows = list(query_job.result())
    
    print(f"🔍 get_total_mau: Query returned {len(rows)} rows")
    for row in rows:
        print(f"  Row: {row}")

    data_mau = {}
    for row in rows:
        if row.product == "Netmonk":
            data_mau["total_mau_netmonk"] = row.total_mau_formatted
            data_mau["mau_percentage_netmonk"] = row.mau_percentage_formatted
            data_mau["growth_mau_netmonk"] = row.growth_mau
        elif row.product == "Netmonk Prime":
            data_mau["total_mau_prime"] = row.total_mau_formatted
            data_mau["mau_percentage_prime"] = row.mau_percentage_formatted
            data_mau["growth_mau_prime"] = row.growth_mau
        elif row.product == "Netmonk HI":
            data_mau["total_mau_hi"] = row.total_mau_formatted
            data_mau["mau_percentage_hi"] = row.mau_percentage_formatted
            data_mau["growth_mau_hi"] = row.growth_mau
    
    print(f"📊 Final data_mau: {data_mau}")
    return data_mau

def get_order_progress():
    client = bigquery.Client.from_service_account_json("service_account.json")

    QUERY = """
WITH monthly_data AS (
  SELECT
    DATE_TRUNC(order_created_date, MONTH) AS order_month,
    COUNT(order_id) AS total_orders,
    COUNTIF(fulfillment_status = "Closed by Netmonk") AS total_completed,
    COUNTIF(fulfillment_status NOT IN ("Canceled Order", "Review Order", "Closed by Netmonk")) AS total_on_progress
  FROM `L4_datamart.order_ncx`
  WHERE fulfillment_status NOT IN ("Canceled Order", "Review Order")
    AND DATE_TRUNC(order_created_date, MONTH) IN (
      DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH), MONTH),
      DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
    )
  GROUP BY order_month
),
growth_calc AS (
  SELECT
    order_month,
    total_orders,
    total_completed,
    total_on_progress,
    ROUND(
      (total_orders - LAG(total_orders) OVER (ORDER BY order_month)) 
      / LAG(total_orders) OVER (ORDER BY order_month) * 100, 2
    ) AS growth_percentage,
    ROUND(total_completed / total_orders * 100, 2) AS completed_percentage,
    ROUND(total_on_progress / total_orders * 100, 2) AS on_progress_percentage
  FROM monthly_data
),
formatted AS (
  SELECT
    order_month,
    REPLACE(FORMAT("%'d", total_orders), ",", ".") AS total_orders_formatted,
    REPLACE(FORMAT("%'d", total_completed), ",", ".") AS total_completed_formatted,
    REPLACE(FORMAT("%'d", total_on_progress), ",", ".") AS total_on_progress_formatted,
    CASE 
      WHEN growth_percentage > 0 THEN CONCAT('meningkat sebanyak ', FORMAT("%.2f", growth_percentage), '%')
      WHEN growth_percentage < 0 THEN CONCAT('menurun sebanyak ', FORMAT("%.2f", ABS(growth_percentage)), '%')
      ELSE 'Tetap 0%'
    END AS growth_percentage_formatted,
    FORMAT("%.2f%%", growth_percentage) AS growth_percentage_formatted,
    FORMAT("%.2f%%", completed_percentage) AS completed_percentage_formatted,
    FORMAT("%.2f%%", on_progress_percentage) AS on_progress_percentage_formatted
  FROM growth_calc
)
SELECT *
FROM formatted
WHERE order_month = DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH);
"""

    query_job = client.query(QUERY)
    rows = list(query_job.result())
    
    print(f"🔍 get_order_progress: Query returned {len(rows)} rows")
    for row in rows:
        print(f"  Row: {row}")

    data_orders = {}
    if rows:
        row = rows[0]  # ambil bulan terbaru
        data_orders["total_orders"] = row.total_orders_formatted
        data_orders["growth_orders"] = row.growth_percentage_formatted
        data_orders["total_completed_orders"] = row.total_completed_formatted
        data_orders["completed_orders_percentage"] = row.completed_percentage_formatted
        data_orders["total_on_progress_orders"] = row.total_on_progress_formatted
        data_orders["on_progress_orders_percentage"] = row.on_progress_percentage_formatted
    
    print(f"📊 Final data_orders: {data_orders}")
    return data_orders

def get_category_order():
    client = bigquery.Client.from_service_account_json("service_account.json")

    QUERY = """
WITH base_data AS (
  SELECT
    fulfillment_status,
    product,
    regional
  FROM `L4_datamart.order_ncx`
  WHERE DATE_TRUNC(order_created_date, MONTH) = DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
),
status_summary AS (
  SELECT
    fulfillment_status,
    FORMAT('%d', COUNT(*)) AS total_orders -- ubah ke string
  FROM base_data
  WHERE fulfillment_status = 'Butuh Dokumen Kontrak/BA Split'
  GROUP BY fulfillment_status
),
product_summary AS (
  SELECT
    product,
    FORMAT('%d', COUNT(*)) AS total_orders, -- ubah ke string
    FORMAT('%.2f', SAFE_DIVIDE(COUNT(*), SUM(COUNT(*)) OVER()) * 100) AS percentage -- string dengan 2 decimal
  FROM base_data
  WHERE product IN ('Netmonk Prime', 'Netmonk HI')
    AND fulfillment_status NOT IN ('Review Order', 'Canceled Order', 'Closed by Netmonk')
  GROUP BY product
),
regional_summary AS (
  SELECT
    regional,
    FORMAT('%d', COUNT(*)) AS total_orders -- ubah ke string
  FROM base_data
  WHERE fulfillment_status NOT IN ('Review Order', 'Canceled Order', 'Closed by Netmonk')
  GROUP BY regional
  ORDER BY CAST(total_orders AS INT64) DESC
  LIMIT 1
)
SELECT
  'status' AS category,
  fulfillment_status AS label,
  total_orders,
  NULL AS percentage
FROM status_summary

UNION ALL

SELECT
  'product' AS category,
  product AS label,
  total_orders,
  percentage
FROM product_summary

UNION ALL

SELECT
  'regional' AS category,
  regional AS label,
  total_orders,
  NULL AS percentage
FROM regional_summary
"""

    rows = list(client.query(QUERY).result())
    
    print(f"🔍 get_category_order: Query returned {len(rows)} rows")
    for row in rows:
        print(f"  Row: {row}")

    # Ubah ke dictionary, bukan list
    order_category = {}

    for row in rows:
        if row.category == "status":
            order_category['contract_document'] = row.total_orders

        elif row.category == "product":
            if row.label == "Netmonk Prime":
                order_category['remaining_order_prime'] = row.total_orders
            elif row.label == "Netmonk HI":
                order_category['remaining_order_hi'] = row.total_orders

        elif row.category == "regional":
            order_category['remaining_order_regional'] = row.label
            order_category['total_remaining_order_regional'] = row.total_orders
    
    print(f"📊 Final order_category: {order_category}")
    return order_category

def get_total_devices():
    client = bigquery.Client.from_service_account_json("service_account.json")

    QUERY = """
    WITH monthly AS (
      -- Prime
      SELECT
        'prime' AS product_type,
        DATE_TRUNC(date, MONTH) AS month,
        MAX(cumulative_prime_network)
          + MAX(cumulative_prime_server)
          + MAX(cumulative_prime_website) AS total_devices
      FROM `L4_datamart.netmonk_daily_metrics`
      WHERE DATE_TRUNC(date, MONTH) IN (
        DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH),
        DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH), MONTH)
      )
        AND customer_type = 'non sda'
      GROUP BY month

      UNION ALL

      -- HI
      SELECT
        'hi' AS product_type,
        DATE_TRUNC(date, MONTH) AS month,
        MAX(cumulative_hsi_devices) AS total_devices
      FROM `L4_datamart.netmonk_daily_metrics`
      WHERE DATE_TRUNC(date, MONTH) IN (
        DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH),
        DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH), MONTH)
      )
        AND customer_type = 'non sda'
      GROUP BY month
    ),

    calc AS (
      SELECT
        product_type,
        month,
        total_devices,
        LAG(total_devices) OVER(
          PARTITION BY product_type
          ORDER BY month
        ) AS prev_total_devices
      FROM monthly
    )

    SELECT
      product_type,
      REPLACE(FORMAT("%'d", total_devices), ",", ".") AS total_devices_fmt,
      ROUND(
        (total_devices - prev_total_devices) / prev_total_devices * 100,
        2
      ) AS growth_percentage
    FROM calc
    WHERE month = DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH);
    """

    rows = list(client.query(QUERY).result())
    
    print(f"🔍 get_total_devices: Query returned {len(rows)} rows")
    for row in rows:
        print(f"  Row: {row}")
    
    data_devices = {}

    for row in rows:
        growth = row.growth_percentage

        if row.product_type == "prime":
            data_devices["total_devices_prime"] = row.total_devices_fmt
            if growth is None:
                data_devices["growth_devices_prime"] = "Tetap 0%"
            elif growth > 0:
                data_devices["growth_devices_prime"] = f"meningkat sebanyak {growth}%"
            elif growth < 0:
                data_devices["growth_devices_prime"] = f"menurun sebanyak {abs(growth)}%"
            else:
                data_devices["growth_devices_prime"] = "Tetap 0%"

        elif row.product_type == "hi":
            data_devices["total_devices_hi"] = row.total_devices_fmt
            if growth is None:
                data_devices["growth_devices_hi"] = "Tetap 0%"
            elif growth > 0:
                data_devices["growth_devices_hi"] = f"meningkat sebanyak {growth}%"
            elif growth < 0:
                data_devices["growth_devices_hi"] = f"menurun sebanyak {abs(growth)}%"
            else:
                data_devices["growth_devices_hi"] = "Tetap 0%"
    
    print(f"📊 Final data_devices: {data_devices}")
    return data_devices
