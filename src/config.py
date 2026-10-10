"""Shared Snowflake configuration for the retail analytics pipeline."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


SNOWFLAKE_USER = _required("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = _required("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = _required("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "RETAIL_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "RETAIL_DB")
SNOWFLAKE_RAW_SCHEMA = os.getenv("SNOWFLAKE_RAW_SCHEMA", "RAW")
SNOWFLAKE_ANALYTICS_SCHEMA = os.getenv("SNOWFLAKE_ANALYTICS_SCHEMA", "ANALYTICS")


def connector_kwargs(schema: str | None = None) -> dict:
    return {
        "user": SNOWFLAKE_USER,
        "password": SNOWFLAKE_PASSWORD,
        "account": SNOWFLAKE_ACCOUNT,
        "warehouse": SNOWFLAKE_WAREHOUSE,
        "database": SNOWFLAKE_DATABASE,
        "schema": schema or SNOWFLAKE_RAW_SCHEMA,
    }
