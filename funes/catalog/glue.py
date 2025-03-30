import os
from dataclasses import dataclass
from typing import Any, Literal

from boto3 import Session
from pydantic import Field, model_serializer
from pyiceberg.catalog import load_catalog

from funes.catalog.base import CatalogClient, CatalogSettings


class GlueCatalogSettings(CatalogSettings):
    """
    Settings for the Glue Catalog.

    The generated settings work with:
    - A Glue Catalog
    - An s3 bucket

    Args:
        name: Name of the AWS Glue database.
        type: Type of the catalog.

    """

    name: str
    type: Literal["glue"] = "glue"
    session: Session = Field(default_factory=Session)

    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        # Without doing this, it fails
        # https://github.com/apache/iceberg-python/issues/1775
        if credentials := self.session.get_credentials():
            os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
            os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
            if credentials.token:
                os.environ["AWS_SESSION_TOKEN"] = credentials.token

            credentials_properties = {
                "access-key-id": credentials.access_key,
                "secret-access-key": credentials.secret_key,
                "session-token": credentials.token,
            }

        return {
            "name": self.name,
            "type": self.type,
            "glue.profile-name": self.session.profile_name,
            "glue.region": self.session.region_name,
            "glue.access-key-id": credentials_properties["access-key-id"],
            "glue.secret-access-key": credentials_properties["secret-access-key"],
            "glue.session-token": credentials_properties["session-token"],
        }


@dataclass(frozen=True)
class GlueCatalogClient(CatalogClient):
    @classmethod
    def initialize(cls, settings: CatalogSettings) -> "GlueCatalogClient":
        catalog = load_catalog(**settings.model_dump())
        return GlueCatalogClient(catalog=catalog)
