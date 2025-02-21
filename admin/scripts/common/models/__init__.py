from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Choice(str, Enum):
    yes = "Yes"
    not_planned = "Not planned"
    not_yet = "Not yet"


class Choice2(str, Enum):
    yes = "Yes"
    not_sure_yet = "Not sure yet"
    no = "No"


class ChoiceReminder(str, Enum):
    no = "No"
    yes_one_week = "Yes, in one week"
    yes_one_month = "Yes, in one month"


class ProjectRole(str, Enum):
    principal_author_lead_engineer = "Principal author / lead engineer"
    core_contributor_maintainer = "Core contributor / maintainer"
    release_manager = "Release manager"
    security = "Security"
    infrastructure_devops = "Infrastructure/DevOps"
    community_manager = "Community manager"
    outreach_coordinator = "Outreach coordinator"
    other = "Other"


class Form(BaseModel):
    class Response(BaseModel):
        time: str = Field(alias="_time")
        author_name: str = Field(alias="_name")
        name: str = Field(alias="q1")
        role: ProjectRole | list[ProjectRole] = Field(alias="q2")
        build_failure_duration: str = Field(alias="q3")
        dependency_update: Choice = Field(alias="q4")
        contributors: str = Field(alias="q6")
        q24: Optional[Choice2] = Field(alias="q24", default=None)
        reminder: Optional[ChoiceReminder] = Field(alias="q25", default=None)

    questions: dict[str, str]
    responses: list[Response]


class Project(BaseModel):
    class Author(BaseModel):
        author_name: str
        role: ProjectRole | list[ProjectRole]

    class CI_CD(BaseModel):
        build_failure_duration: str
        dependency_update: Choice

    name: str
    author: Author
    contributors: str
    build_system: CI_CD
