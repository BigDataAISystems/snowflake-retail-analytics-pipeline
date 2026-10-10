"""Load the Online Retail CSV into Snowflake's RAW layer in bounded-memory batches."""

from pathlib import Path
import argparse

import pandas as pd
import snowflake.connector

from config import ROOT_DIR, SNOWFLAKE_RAW_SCHEMA, connector_kwargs

COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country",
]


def clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize types while preserving source-level nulls for the RAW layer."""
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], format="%m/%d/%y %H:%M", errors="coerce"
    )
    df = df.dropna(subset=["InvoiceDate"])
    df["InvoiceDate"] = df["InvoiceDate"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df[COLUMNS].astype(object)
    return df.where(pd.notnull(df), None)


def load_csv(csv_path: Path, batch_size: int = 10_000) -> int:
    insert_sql = f"""
        INSERT INTO {SNOWFLAKE_RAW_SCHEMA}.retail_raw
        (invoice_no, stock_code, description, quantity, invoice_date,
         unit_price, customer_id, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    total_inserted = 0
    conn = snowflake.connector.connect(**connector_kwargs(SNOWFLAKE_RAW_SCHEMA))
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {SNOWFLAKE_RAW_SCHEMA}.retail_raw")
            print(f"Truncated {SNOWFLAKE_RAW_SCHEMA}.retail_raw")

            for chunk in pd.read_csv(csv_path, encoding="latin1", chunksize=batch_size):
                cleaned = clean_chunk(chunk)
                rows = list(cleaned.itertuples(index=False, name=None))
                if not rows:
                    continue
                cursor.executemany(insert_sql, rows)
                total_inserted += len(rows)
                print(f"Inserted {total_inserted:,} rows")
        conn.commit()
    finally:
        conn.close()

    return total_inserted


def main() -> None:
    parser = argparse.ArgumentParser(description="Load Online Retail data into Snowflake.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=ROOT_DIR / "data" / "Online_Retail.csv",
        help="Path to the Online Retail CSV file.",
    )
    parser.add_argument("--batch-size", type=int, default=10_000)
    args = parser.parse_args()

    if not args.csv.exists():
        raise FileNotFoundError(
            f"Dataset not found: {args.csv}\nSee data/README.md for setup instructions."
        )

    count = load_csv(args.csv, args.batch_size)
    print(f"Load complete: {count:,} rows inserted.")


if __name__ == "__main__":
    main()
