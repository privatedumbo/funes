# funes

[![Release](https://img.shields.io/github/v/release/privatedumbo/funes)](https://img.shields.io/github/v/release/privatedumbo/funes)
[![Build status](https://img.shields.io/github/actions/workflow/status/privatedumbo/funes/main.yml?branch=main)](https://github.com/privatedumbo/funes/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/privatedumbo/funes/branch/main/graph/badge.svg)](https://codecov.io/gh/privatedumbo/funes)
[![Commit activity](https://img.shields.io/github/commit-activity/m/privatedumbo/funes)](https://img.shields.io/github/commit-activity/m/privatedumbo/funes)
[![License](https://img.shields.io/github/license/privatedumbo/funes)](https://img.shields.io/github/license/privatedumbo/funes)

Storing datasets with Iceberg and reading them with DuckDB.

## Usage

```python
import polars as pl

from funes.catalog.glue import GlueCatalogClient
from funes.client.core import Funes
from funes.query.duckdb import DuckDBQueryEngine


catalog_client = GlueCatalogClient(...)
duckdb_client = DuckDBQueryEngine(...)
funes = Funes(catalog_client=catalog_client, duckdb_client=duckdb_client)

# Create sample data
dataset = pl.DataFrame({"id": range(1000), "value": [i * 2 for i in range(1000)]})

funes.write_and_register_dataframe(dataset, table="table_name")
funes.query("SELECT * FROM table_name")

```
