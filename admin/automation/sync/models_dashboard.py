from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class Fund(BaseModel):
    @dataclass
    class Subgrant(BaseModel):
        @dataclass
        class Properties(BaseModel):
            @dataclass
            class Webpage(BaseModel):
                name: Optional[str] = Field(
                    default=None,
                    alias="sitename",
                    description="Symbolic name for the subgrant, as shown under https://nlnet.nl/project",
                    examples=["GNUnet-CONG"],
                )
                summary: str

            webpage: Webpage

        @dataclass
        class Proposal(BaseModel):
            @dataclass
            class Websites(BaseModel):
                website: List[str]

            @dataclass
            class Contact(BaseModel):
                name: str
                email: str
                organisationName: str

            websites: Websites
            contact: Contact

        properties: Properties
        proposal: Proposal

    subgrants: List[Subgrant] = Field(
        alias="proposals",
    )
