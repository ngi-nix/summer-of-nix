from pydantic import BaseModel, Field, field_validator


class Subgrant(BaseModel):
    class Contact(BaseModel):
        name: str
        email: str
        organisationName: str

    @field_validator("fund", mode="before")
    def rename_funds(cls, value: str):
        value = value.replace("_Fund", "")
        value = value.replace("PET", "Review")
        value = value.replace("Discovery", "Review")
        return value

    name: str | None = Field(default=None)
    id: str
    fund: str
    summary: str
    websites: list[str] = []
    contact: Contact

    def test(self):
        return self.contact.name


class Overview(BaseModel):
    name: str | None = None
    summary: str
    websites: list[str] = []


class Project(BaseModel):
    name: str = ""
    subgrants: list[str] = []


class AuthorMessages(BaseModel):
    message: str
    contacted: str
