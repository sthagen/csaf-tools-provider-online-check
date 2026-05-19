from typing import Annotated, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Annotated[
        str,
        Field(description="'healthy' or 'unhealthy'"),
    ]

    free_slots: Annotated[
        int,
        Field(description="Number of available scan slots"),
    ]

    total_slots: Annotated[
        int,
        Field(description="Total number of scan slots"),
    ]

    csaf_checker_available: Annotated[
        bool,
        Field(description="Whether the csaf_checker binary is available"),
    ]

    redis_available: Annotated[
        bool,
        Field(description="Whether Redis is available"),
    ]

    errors: Annotated[
        Optional[list[str]],
        Field(default=None, description="List of error messages if unhealthy"),
    ]
