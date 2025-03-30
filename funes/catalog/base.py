import abc
from dataclasses import dataclass

import narwhals as nw
import pyarrow as pa
from loguru import logger
from narwhals.typing import IntoFrame
from pydantic_settings import BaseSettings
from pyiceberg.catalog import LOCATION, Catalog
from pyiceberg.table import Table


class CatalogSettings(BaseSettings):
    pass


@dataclass(frozen=True)
class CatalogClient(abc.ABC):
    catalog: Catalog

    @property
    def default_location(self) -> str:
        return str(self.catalog.load_namespace_properties(self.catalog.name)[LOCATION])

    @classmethod
    @abc.abstractmethod
    def initialize(cls, settings: CatalogSettings) -> "CatalogClient":
        pass

    @staticmethod
    def schema_for_dataframe(dataset: IntoFrame) -> pa.Schema:
        nw_dataset = nw.from_native(dataset)
        logger.debug(f"Schema: {nw_dataset.schema}")
        return nw_dataset.schema.to_arrow()

    def create_table(self, table_name: str, schema: pa.Schema) -> Table:
        """Create table if it doesn't exist."""
        identifier = (self.catalog.name, table_name)

        exists = self.catalog.table_exists(identifier)
        if exists:
            logger.info(
                f"Table {table_name} already exists in catalog {self.catalog.name}"
            )
            table = self.catalog.load_table(identifier)
        else:
            logger.info(f"Creating table {table_name} in catalog {self.catalog.name}")
            table = self.catalog.create_table(
                identifier=identifier,
                schema=schema,
            )

        return table

    def get_table(self, table_name: str) -> Table:
        identifier = (self.catalog.name, table_name)
        return self.catalog.load_table(identifier)
