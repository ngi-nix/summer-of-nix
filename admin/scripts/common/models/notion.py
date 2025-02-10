from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class Subgrant(BaseModel):
    class Contact(BaseModel):
        name: str
        email: str
        organisationName: str

    @field_validator("fund", mode="before")
    def rename_funds(cls, value):
        value = value.replace("_Fund", "")
        value = value.replace("PET", "Review")
        value = value.replace("Discovery", "Review")
        return value

    name: Optional[str] = Field(default=None)
    id: str
    fund: str
    summary: str
    websites: List[str]
    contact: Contact

    def test(self):
        return self.contact.name


class Overview(BaseModel):
    name: Optional[str] = Field(default=None)
    summary: str
    websites: List[str]


class Project(BaseModel):
    name: str = ""
    subgrants: List[str] = []
