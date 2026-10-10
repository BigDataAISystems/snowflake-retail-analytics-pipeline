# Architecture

The project follows a simple ELT-style analytics architecture.

```mermaid
flowchart TD
    A[Online Retail CSV] --> B[Python ingestion]
    B --> C[(Snowflake RAW<br/>retail_raw)]
    C --> D[SQL staging<br/>stg_retail]
    D --> E[(Analytics tables<br/>orders / customers)]
    E --> F[SQL analytics]
    E --> G[Python / pandas]
    G --> H[Visualization]
```

## Layers

### Raw
`RAW.RETAIL_RAW` preserves source-level records after only datatype normalization required for loading.

### Staging
`ANALYTICS.STG_RETAIL` filters invalid business records (`quantity <= 0`, `unit_price <= 0`, and missing customer IDs) and derives `line_total`.

### Analytics
`ANALYTICS.ORDERS` aggregates invoice-level order totals, while `ANALYTICS.CUSTOMERS` creates customer-level order and lifetime-value metrics.

### Consumption
SQL queries and Python scripts consume the analytics layer for analysis and visualization.
