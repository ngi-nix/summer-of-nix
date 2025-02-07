from typing import List, Optional

from pydantic import BaseModel, Field


class Fund(BaseModel):
    class Subgrant(BaseModel):
        class Properties(BaseModel):
            class Webpage(BaseModel):
                name: Optional[str] = Field(
                    default=None,
                    alias="sitename",
                    description="Symbolic name for the subgrant, as shown under https://nlnet.nl/project",
                    examples=["GNUnet-CONG"],
                )
                summary: str

            webpage: Webpage

        class Proposal(BaseModel):
            class Websites(BaseModel):
                website: List[str]

            class Contact(BaseModel):
                name: str
                email: str
                organisationName: str

            websites: Websites
            contact: Contact

        properties: Properties
        proposal: Proposal

    subgrants: List[Subgrant] = Field(alias="proposals")
