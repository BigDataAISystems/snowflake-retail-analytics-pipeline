# Dataset

This project uses the **Online Retail** transactional dataset used by the original repository.
The raw CSV is intentionally not tracked in Git because it is large.

Place the dataset at:

```text
data/Online_Retail.csv
```

Expected columns:

```text
InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
```

The loader expects the source `InvoiceDate` values in the format `MM/DD/YY HH:MM` and reads the file using `latin1` encoding, matching the dataset used in the original project.
