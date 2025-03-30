from dataclasses import dataclass
from typing import Any

from duckdb import DuckDBPyRelation


@dataclass(frozen=True)
class QueryResult:
    result: DuckDBPyRelation

    def __getattr__(self, item: str) -> Any:
        """Delegate attribute access to the underlying duckdb relation."""
        return getattr(self.result, item)
