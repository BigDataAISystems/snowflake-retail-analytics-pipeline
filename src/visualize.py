"""Create and save a monthly revenue visualization from Snowflake analytics data."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

from config import (
    ROOT_DIR,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_ANALYTICS_SCHEMA,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_USER,
    SNOWFLAKE_WAREHOUSE,
)

QUERY = f"""
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(order_total) AS revenue
FROM {SNOWFLAKE_ANALYTICS_SCHEMA}.orders
GROUP BY month
ORDER BY month;
"""


def main() -> None:
    engine = create_engine(
        URL(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_ANALYTICS_SCHEMA,
            warehouse=SNOWFLAKE_WAREHOUSE,
        )
    )
    try:
        df = pd.read_sql(QUERY, engine)
    finally:
        engine.dispose()

    df.columns = [column.upper() for column in df.columns]
    output = ROOT_DIR / "results" / "monthly_revenue.png"
    output.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df["MONTH"], df["REVENUE"], marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"Saved visualization to {output}")


if __name__ == "__main__":
    main()
