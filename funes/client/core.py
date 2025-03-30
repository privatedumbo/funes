from dataclasses import dataclass
from pathlib import Path

import narwhals as nw
from loguru import logger
from narwhals.dependencies import is_narwhals_lazyframe
from narwhals.typing import IntoFrame
from pyiceberg.table import Table

from funes.catalog.base import CatalogClient
from funes.query.duckdb import DuckDBQueryEngine
from funes.query.result import QueryResult

template_path = Path(__file__).parent.parent / "templates" / "duckdb.template"


@dataclass(frozen=True)
class Funes:
    catalog_client: CatalogClient
    duckdb_client: DuckDBQueryEngine

    def write_and_register_dataframe(self, dataset: IntoFrame, *, table: str) -> None:
        """
        Write a dataset to a table and register it in the iceberg catalog.

        After having registered a dataset, it can be queried using the `query` method.
        """
        self.write_dataframe(dataset, table=table)
        self.register_table(table)

    def query(self, query: str) -> QueryResult:
        """
        Execute a query.

        Queries can be executed against registered tables.

        """
        return self.duckdb_client.query(query)

    def write_dataframe(self, dataset: IntoFrame, *, table: str) -> None:
        iceberg_table = self._create_table_if_not_exists(table, dataset)
        self._update_table(iceberg_table, dataset)

    def register_table(self, table: str) -> None:
        location = self.catalog_client.default_location
        logger.info(f"Registering table {table}")
        self.duckdb_client.register_table(table, location)
        logger.info(f"Table {table} registered")

    def _create_table_if_not_exists(self, table: str, dataset: IntoFrame) -> Table:
        dataset_schema = self.catalog_client.schema_for_dataframe(dataset)
        return self.catalog_client.create_table(table_name=table, schema=dataset_schema)

    def _update_table(self, table: Table, dataset: IntoFrame) -> None:
        any_dataset = nw.from_native(dataset)
        if is_narwhals_lazyframe(any_dataset):
            any_dataset = any_dataset.collect()

        logger.info(f"Updating table {table.name()[1]}")
        table.append(df=any_dataset.to_arrow())
        logger.info(f"Table {table.name()[1]} updated")
