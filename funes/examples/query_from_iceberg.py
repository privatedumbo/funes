from pathlib import Path

import polars as pl

from funes.catalog.glue import GlueCatalogClient, GlueCatalogSettings
from funes.client.core import Funes
from funes.query.duckdb import DuckDBQueryEngine


def get_glue_catalog_client() -> GlueCatalogClient:
    glue_catalog_name = "funes"
    settings = GlueCatalogSettings(name=glue_catalog_name)
    return GlueCatalogClient.initialize(settings)


def get_duckdb_client() -> DuckDBQueryEngine:
    duckdb_database = Path(__file__).parent.parent.parent / "funes.db"
    return DuckDBQueryEngine.initialize(duckdb_database)


client = get_glue_catalog_client()
duckdb_client = get_duckdb_client()
funes = Funes(
    catalog_client=client,
    duckdb_client=duckdb_client,
)

# Create sample data
dataset = pl.DataFrame({"id": range(1000), "value": [i * 2 for i in range(1000)]})

funes.write_and_register_dataframe(dataset, table="table_name")
result = funes.query("SELECT * FROM table_name")
result.show()
