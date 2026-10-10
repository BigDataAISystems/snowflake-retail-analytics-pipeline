"""Run lightweight post-load quality checks on the Snowflake RAW table."""

import snowflake.connector

from config import SNOWFLAKE_RAW_SCHEMA, connector_kwargs

CHECKS = {
    "row_count": f"SELECT COUNT(*) FROM {SNOWFLAKE_RAW_SCHEMA}.retail_raw",
    "invoice_date_range": (
        f"SELECT MIN(invoice_date), MAX(invoice_date) "
        f"FROM {SNOWFLAKE_RAW_SCHEMA}.retail_raw"
    ),
    "null_customer_ids": (
        f"SELECT COUNT(*) FROM {SNOWFLAKE_RAW_SCHEMA}.retail_raw "
        "WHERE customer_id IS NULL"
    ),
    "unit_price_summary": (
        f"SELECT MIN(unit_price), MAX(unit_price), AVG(unit_price) "
        f"FROM {SNOWFLAKE_RAW_SCHEMA}.retail_raw"
    ),
}


def main() -> None:
    conn = snowflake.connector.connect(**connector_kwargs(SNOWFLAKE_RAW_SCHEMA))
    try:
        with conn.cursor() as cursor:
            for name, sql in CHECKS.items():
                cursor.execute(sql)
                print(f"{name}: {cursor.fetchone()}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
