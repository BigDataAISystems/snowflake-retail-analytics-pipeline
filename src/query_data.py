"""Run a sample analytics query against the Snowflake analytics layer."""

import pandas as pd
import snowflake.connector

from config import SNOWFLAKE_ANALYTICS_SCHEMA, connector_kwargs

QUERY = f"""
SELECT country, SUM(lifetime_value) AS revenue
FROM {SNOWFLAKE_ANALYTICS_SCHEMA}.customers
GROUP BY country
ORDER BY revenue DESC;
"""


def main() -> None:
    conn = snowflake.connector.connect(**connector_kwargs(SNOWFLAKE_ANALYTICS_SCHEMA))
    try:
        df = pd.read_sql(QUERY, conn)
        print(df.head(10).to_string(index=False))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
