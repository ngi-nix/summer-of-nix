from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


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


class ChoiceAgreement(str, Enum):
    STRONGLY_DISAGREE = "Strongly disagree"
    DISAGREE = "Disagree"
    DONT_KNOW = "Don't know/neutral"
    AGREE = "Agree"
    STRONGLY_AGREE = "Strongly agree"


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


class ProjectArtefact(str, Enum):
    EXECUTABLES = "Executables"
    LIBRARIES = "Librares"  # NOTE: question entry has a typo
    SERVICES = "Services"


class ContactChannel(str, Enum):
    EMAIL = "Email"
    MATRIX = "Matrix"
    GITHUB = "Github"
    OTHER = "Other"


class ReleasePeriod(str, Enum):
    NO_YEAR = "There are no stable releases yet"
    UNDER_1_YEAR = "<1 year"
    OVER_1_YEAR = ">1 year"
    OVER_5_YEAR = ">5 years"
    OVER_10_YEAR = ">10 years"
    OVER_20_YEAR = ">20 years"


class Form(BaseModel):
    class Response(BaseModel):
        @field_validator(
            "survey_with_structured_data", "extensions_exist", mode="before"
        )
        def map_yes_no_to_bool(cls, value: str) -> bool:
            if value.lower() == "yes":
                return True
            return False

        @field_validator("contributors", mode="before")
        def map_contributors(cls, value: str) -> float | None:
            if value.replace(".", "", 1).isdigit():
                return float(value)
            return None

        # survey
        time: str = Field(alias="_time")
        survey_reminder: Optional[ChoiceReminder] = Field(default=None, alias="q25")
        survey_feedback: str = Field(alias="q45")
        survey_with_structured_data: bool = Field(default=False, alias="q24")

        # metadata
        project_name: str = Field(alias="q1")
        repository: str = Field(alias="q42")
        contributors: int | None = Field(alias="q6")

        # author
        author_name: str = Field(alias="_name")
        author_role: list[AuthorRole] = Field(alias="q2")
        author_contact_channels: list[ContactChannel] = Field(alias="q22")
        author_contact: str = Field(alias="q23")

        # longevity
        duration_stable_release: ReleasePeriod = Field(alias="q11")
        duration_future_maintenance: ReleasePeriod = Field(alias="q12")

        # infra
        duration_build_failure: str = Field(alias="q3")
        dependency_update_automatic: Choice = Field(alias="q4")
        dependency_update_frequency: UpdateFrequency = Field(alias="q5")
        devenv_setup_time: DevenvSetupTimes = Field(alias="q7")
        personal_deployment: Optional[str] = Field(default=None, alias="q35")
        dependency_management: str = Field(alias="q43")
        project_framework: str = Field(alias="q44")

        # Nix
        nix_familiarity: NixFamiliarity = Field(alias="q8")
        nix_dev_env: Choice = Field(alias="q9")
        nix_ci_cd: Choice = Field(alias="q10")
        nix_onboard: ChoiceAgreement = Field(alias="q13")
        nix_maintain: ChoiceAgreement = Field(alias="q14")
        nix_discover: ChoiceAgreement = Field(alias="q15")
        nix_self_host: str = Field(alias="q16")
        nix_installation: str = Field(alias="q17")
        nix_adoption: str = Field(alias="q18")
        nix_retention: str = Field(alias="q19")
        nix_other_uses: str = Field(alias="q20")
        nix_pairing: Choice2 = Field(alias="q21")

        # nixos
        nixos_artefacts: list[ProjectArtefact] = Field(alias="q37")
        nixos_package_name: str = Field(alias="q38")  # or service
        nixos_maintainer: Optional[str] = Field(default=None, alias="q39")

        # artefacts
        libraries_exist: Optional[str] = Field(default=None, alias="q26")
        programs_cli: Optional[str] = Field(default=None, alias="q28")
        programs_gui: Optional[str] = Field(default=None, alias="q29")
        mobile_apps: Optional[str] = Field(default=None, alias="q31")
        services: Optional[str] = Field(default=None, alias="q32")
        extensions_exist: bool = Field(default=False, alias="q36")

        # documentation
        documentation_libraries: str = Field(alias="q27")
        documentation_programs: str = Field(alias="q30")
        documentation_services: str = Field(alias="q33")
        specification_document: Optional[str] = Field(default=None, alias="q34")
        documentation_nixos: Optional[str] = Field(default=None, alias="q40")
        documentation_source: str = Field(alias="q41")

    questions: dict[str, str]
    responses: list[Response]


class Project(BaseModel):
    class Metadata(BaseModel):
        class Author(BaseModel):
            class Survey(BaseModel):
                reminder: Optional[ChoiceReminder]
                feedback: str

            name: str
            role: list[AuthorRole]
            contact_channels: list[ContactChannel]
            contact: str
            available_for_pairing: Choice2
            nix_familiarity: NixFamiliarity
            survey: Survey

        repository: str
        contributors: int
        author: Author
        stable_release_start: str
        expected_longevity: str

    class Infrastructure(BaseModel):
        class CI_CD(BaseModel):
            build_failure_duration: str
            dependency_update: str
            with_nix: Choice

        class DevEnv(BaseModel):
            setup_time: str
            with_nix: Choice

        ci_cd: CI_CD
        devenv: DevEnv

    class Nix(BaseModel):
        can_ease_onboarding: ChoiceAgreement
        can_help_maintainability: ChoiceAgreement
        can_help_discoverability: ChoiceAgreement

    name: str
    meta: Metadata
    infra: Infrastructure
    nix: Nix


def project_from_response(
    resp: Form.Response,
) -> tuple[Project | None, str]:
    if resp.contributors is None:
        return (None, "contributors")

    project = Project(
        name=resp.project_name,
        meta=Project.Metadata(
            repository=resp.repository,
            contributors=resp.contributors,
            author=Project.Metadata.Author(
                name=resp.author_name,
                role=resp.author_role,
                contact_channels=resp.author_contact_channels,
                contact=resp.author_contact,
                available_for_pairing=resp.nix_pairing,
                nix_familiarity=resp.nix_familiarity,
                survey=Project.Metadata.Author.Survey(
                    feedback=resp.survey_feedback,
                    reminder=resp.survey_reminder,
                ),
            ),
            stable_release_start=resp.duration_stable_release,
            expected_longevity=resp.duration_future_maintenance,
        ),
        infra=Project.Infrastructure(
            ci_cd=Project.Infrastructure.CI_CD(
                build_failure_duration=resp.duration_build_failure,
                dependency_update=resp.dependency_update_automatic,
                with_nix=resp.nix_ci_cd,
            ),
            devenv=Project.Infrastructure.DevEnv(
                setup_time=resp.devenv_setup_time,
                with_nix=resp.nix_dev_env,
            ),
        ),
        nix=Project.Nix(
            can_ease_onboarding=resp.nix_onboard,
            can_help_maintainability=resp.nix_maintain,
            can_help_discoverability=resp.nix_discover,
        ),
    )

    return (project, "")
