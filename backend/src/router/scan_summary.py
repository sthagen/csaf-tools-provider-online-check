from typing import Annotated

from pydantic import BaseModel, Field


class ScanSummary(BaseModel):
    task_id: Annotated[
        str,
        Field(description="UUID of the scan task"),
    ]

    domain: Annotated[
        str,
        Field(description="Domain that was scanned"),
    ]

    start_time: Annotated[
        int,
        Field(description="Unix timestamp when the scan started"),
    ]

    end_time: Annotated[
        int,
        Field(description="Unix timestamp when the scan finished"),
    ]

    duration: Annotated[
        int,
        Field(description="Scan duration in seconds"),
    ]
