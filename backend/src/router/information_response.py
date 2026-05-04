from typing import Annotated

from pydantic import BaseModel, Field


class InformationResponse(BaseModel):
    csaf_checker_version: Annotated[
        str,
        Field(description="CSAF Checker version used by the provider"),
    ]

    csaf_validator_version: Annotated[
        str,
        Field(description="CSAF Validator version used by the provider"),
    ]

    csaf_provider_version: Annotated[
        str,
        Field(description="Version of the csaf provider"),
    ]

    docs: Annotated[
        str,
        Field(description="API path to docs"),
    ]

    openapi: Annotated[
        str,
        Field(description="API path to OpenAPI JSON file"),
    ]
