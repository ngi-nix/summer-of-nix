from typing import List, Optional

from pydantic import BaseModel, Field


class Subgrant(BaseModel):
    class Contact(BaseModel):
        name: str
        email: str
        organisationName: str

    name: Optional[str] = Field(default=None)
    websites: List[str]
    summary: str
    contact: Contact

    def test(self):
        return self.contact.name


class Project(BaseModel):
    name: str = ""
    subgrants: List[str] = []
