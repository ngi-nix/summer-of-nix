from typing import List, Optional

from pydantic import BaseModel, Field


class Subgrant(BaseModel):
    class Contact(BaseModel):
        name: str
        email: str
        organisationName: str

    name: Optional[str] = Field(default=None)
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


class AuthorMessages(BaseModel):
    message: str
    contacted: str
