from enum import Enum
from operator import itemgetter
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


class DevenvSetupTimes(str, Enum):
    UNDER_10_MIN = "<10 min"
    UNDER_30_MIN = "<30 min"
    UNDER_1_HOUR = "<1h"
    UNDER_4_HOUR = "<4h"
    OVER_4_HOUR = ">4h"


class NixFamiliarity(str, Enum):
    DONT_KNOW = "I don’t know anything about it"
    DONT_USE = "Have learned a few things about it but don’t use it"
    TRIED = "I have tried using Nix or NixOS"
    REGULAR_USER = "I use Nix or NixOS regularly"
    NIXPKGS_CONTRIBUTOR = "I already contributed to Nixpkgs"
    NIXPKGS_MAINTAINER = "I maintain software in Nixpkgs"


# NOTE:
# This is a bidirectional mapping between the questions and the data fields,
# which not only makes it possible to access one from another, but also makes
# setting field aliases much cleaner.
alias_mapping = {
    "q1": "project_name",
    "q2": "author_role",
    "q3": "build_failure_duration",
    "q4": "automatic_dependency_update",
    "q5": "dependency_update_frequency",
    "q6": "contributors",
    "q7": "devenv_setup_time",
    "q8": "nix_familiarity",
    "q9": "nix_dev_env",
    "q24": "structured_data_provided",
    "q25": "reminder",
    "q36": "has_extensions",
}


class Form(BaseModel):
    class Response(BaseModel):
        @model_validator(mode="before")
        def map_aliases(cls, values: dict[str, Any]) -> dict[str, Any]:
            for alias, field_name in alias_mapping.items():
                if alias in values:
                    values[field_name] = values.pop(alias)
            return values

        @field_validator(*itemgetter("q24", "q36")(alias_mapping), mode="before")
        def map_yes_no_to_bool(cls, value: str) -> bool:
            if value.lower() == "yes":
                return True
            return False

        @field_validator(alias_mapping["q6"], mode="before")
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
        devenv_setup_time: DevenvSetupTimes
        contributors: int | None
        reminder: Optional[ChoiceReminder] = Field(default=None)

        # Nix
        nix_familiarity: NixFamiliarity
        nix_dev_env: Choice

        structured_data_provided: bool = Field(default=False)
        has_extensions: bool = Field(default=False)

    questions: dict[str, str]
    responses: list[Response]


class Project(BaseModel):
    class Author(BaseModel):
        name: str
        role: list[AuthorRole]

    class Infrastructure(BaseModel):
        class CI_CD(BaseModel):
            build_failure_duration: str
            dependency_update: str
            # with_nix: bool

        ci_cd: CI_CD
        devenv_setup_time: str

    class Nix(BaseModel):
        familiarity: NixFamiliarity
        has_dev_env: Choice

    name: str
    author: Author
    contributors: int
    infra: Infrastructure
    nix: Nix


def project_from_response(
    resp: Form.Response,
) -> tuple[Project | None, str]:
    if resp.contributors is None:
        return (None, "contributors")

    project_dict = {
        "name": resp.project_name,
        "author": {
            "name": resp.author_name,
            "role": resp.author_role,
        },
        "contributors": resp.contributors,
        "infra": {
            "ci_cd": {
                "build_failure_duration": resp.build_failure_duration,
                "dependency_update": resp.automatic_dependency_update,
            },
            "devenv_setup_time": resp.devenv_setup_time,
        },
        "nix": {
            "familiarity": resp.nix_familiarity,
            "has_dev_env": resp.nix_dev_env,
        },
    }

    project = Project.model_validate(project_dict)

    return (project, "")
