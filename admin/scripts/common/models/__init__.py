from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class Choice(str, Enum):
    YES = "Yes"
    NOT_PLANNED = "Not planned"
    NOT_YET = "Not yet"


class Choice2(str, Enum):
    YES = "Yes"
    NOT_SURE_YET = "Not sure yet"
    NO = "No"


class ChoiceReminder(str, Enum):
    NO = "No"
    YES_ONE_WEEK = "Yes, in one week"
    YES_ONE_MONTH = "Yes, in one month"


class AuthorRole(str, Enum):
    PRINCIPAL_AUTHOR_LEAD_ENGINEER = "Principal author / lead engineer"
    CORE_CONTRIBUTOR_MAINTAINER = "Core contributor / maintainer"
    RELEASE_MANAGER = "Release manager"
    SECURITY = "Security"
    INFRASTRUCTURE_DEVOPS = "Infrastructure/DevOps"
    COMMUNITY_MANAGER = "Community manager"
    OUTREACH_COORDINATOR = "Outreach coordinator"
    OTHER = "Other"


class UpdateFrequency(str, Enum):
    CANT_SAY = "Can't say"
    MORE_ONCE_PER_DAY = "More than once per day"
    MORE_ONCE_PER_WEEK = "More than once per week"
    MORE_ONCE_PER_MONTH = "More than once per month"
    MORE_ONCE_PER_YEAR = "More than once per year"
    LESS_ONCE_PER_YEAR = "Less than once per year"


# NOTE:
# This is a bidirectional mapping between the questions and the data fields,
# which not only makes it possible to access one from another, but also makes
# setting field aliases much cleaner.
question_alias_mapping = {
    "q1": "project_name",
    "q2": "author_role",
    "q3": "build_failure_duration",
    "q4": "automatic_dependency_update",
    "q5": "dependency_update_frequency",
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

        @field_validator(question_alias_mapping["q6"], mode="before")
        def map_contributors(cls, value: str) -> float | None:
            if value.replace(".", "", 1).isdigit():
                return float(value)
            return None

        time: str = Field(alias="_time")
        author_name: str = Field(alias="_name")
        author_role: list[AuthorRole]
        project_name: str
        build_failure_duration: str
        automatic_dependency_update: Choice
        dependency_update_frequency: UpdateFrequency
        contributors: int | None
        structured_data_provided: bool = Field(default=False)
        reminder: Optional[ChoiceReminder] = Field(default=None)

    questions: dict[str, str]
    responses: list[Response]


class Project(BaseModel):
    class Author(BaseModel):
        author_name: str
        role: list[AuthorRole]

    class CI_CD(BaseModel):
        build_failure_duration: str
        dependency_update: Choice

    name: str
    author: Author
    contributors: int
    build_system: CI_CD
