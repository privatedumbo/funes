# funes

Storing datasets with Iceberg and reading them with DuckDB.

## Usage

```python
import polars as pl

from funes.catalog.glue import GlueCatalogClient
from funes.client.core import Funes
from funes.query.duckdb import DuckDBQueryEngine

# Initialize Funes
catalog_client = GlueCatalogClient(...)
duckdb_client = DuckDBQueryEngine(...)
funes = Funes(catalog_client=catalog_client, duckdb_client=duckdb_client)

# Create sample data
dataset = pl.DataFrame({"id": range(1000), "value": [i * 2 for i in range(1000)]})

# Write and register the dataset
funes.write_and_register_dataframe(dataset, table="table_name")

# Query the dataset
result = funes.query("SELECT * FROM table_name")
result.show()
```
