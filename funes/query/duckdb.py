from dataclasses import dataclass
from pathlib import Path

import duckdb
from duckdb import DuckDBPyConnection
from jinja2 import Template

from funes.query.result import QueryResult

template_path = Path(__file__).parent.parent / "templates" / "duckdb.template"


@dataclass(frozen=True)
class DuckDBQueryEngine:
    duckdb_connection: DuckDBPyConnection

    @classmethod
    def initialize(cls, database_path: Path) -> "DuckDBQueryEngine":
        conn = duckdb.connect(database=database_path)
        return cls(conn)

    def register_table(self, table: str, location: str) -> None:
        content = template_path.read_text()
        template = Template(content)
        rendered = template.render(table_name=table, location=location)
        self.duckdb_connection.sql(rendered)

    def start_ui(self) -> None:
        self.duckdb_connection.execute("CALL start_ui();")

    def query(self, query: str) -> QueryResult:
        authenticate = """CREATE OR REPLACE SECRET (
            TYPE s3,
            PROVIDER credential_chain,
            PROFILE dumbo
        );"""
        self.duckdb_connection.sql(authenticate)
        result = self.duckdb_connection.sql(query)
        return QueryResult(result)
