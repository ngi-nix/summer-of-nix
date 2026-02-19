from pydantic import BaseModel, Field


class Fund(BaseModel):
    class Subgrant(BaseModel):
        class Properties(BaseModel):
            class Webpage(BaseModel):
                name: str | None = Field(
                    default=None,
                    alias="sitename",
                    description="Symbolic name for the subgrant, as shown under https://nlnet.nl/project",
                    examples=["GNUnet-CONG"],
                )
                summary: str

            webpage: Webpage

        class Proposal(BaseModel):
            class Websites(BaseModel):
                website: list[str] = []

            class Contact(BaseModel):
                name: str
                email: str
                organisationName: str

            websites: Websites = Field(default_factory=Websites)
            contact: Contact
            fund: str

        id: str
        properties: Properties
        proposal: Proposal

    subgrants: list[Subgrant] = Field(alias="proposals")
