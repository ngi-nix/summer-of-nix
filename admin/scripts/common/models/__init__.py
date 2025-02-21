from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


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


question_alias_mapping = {
    "q1": "project_name",
    "q2": "author_role",
    "q3": "build_failure_duration",
    "q4": "has_dependency_update",
    "q6": "contributors",
    "q24": "structured_data_provided",
    "q25": "reminder",
}


class Form(BaseModel):
    class Response(BaseModel):
        @model_validator(mode="before")
        def map_aliases(cls, values: dict[str, Any]) -> dict[str, Any]:
            for alias, field_name in question_alias_mapping.items():
                if alias in values:
                    values[field_name] = values.pop(alias)
            return values

        @field_validator(question_alias_mapping["q24"], mode="before")
        def map_yes_no_to_bool(cls, value: str) -> bool:
            if value.lower() == "yes":
                return True
            return False

        time: str = Field(alias="_time")
        author_name: str = Field(alias="_name")
        author_role: ProjectRole | list[ProjectRole]
        project_name: str
        build_failure_duration: str
        has_dependency_update: Choice
        contributors: str
        structured_data_provided: bool = Field(default=False)
        reminder: Optional[ChoiceReminder] = Field(default=None)

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
