#!/usr/bin/env python3

import argparse
import logging
from dataclasses import dataclass, field
from enum import Enum
from time import sleep
from typing import List

import ijson
import pandas as pd
from pandas import Series
from pydantic import BaseModel, ValidationError
from tqdm import tqdm

from lib.ghkit import GitClient
from lib.models.notion import Project, Subgrant
from lib.utils import (
    cleanup_empty,
    cleanup_urls,
    dir_path,
    get_notion_projects,
    load_credentials,
    remove_urls,
    zip_file_type,
)


@dataclass
class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Read project information exported from the NLnet dashboard and Notion, and create one GitHub pull request and milestone per project, based on a template.
            """
        )

        # Positional
        self.parser.add_argument(
            "notion_zip",
            type=zip_file_type,
            help="ZIP file containing the exported data from Notion",
        )
        self.parser.add_argument(
            "dashboard_file",
            type=argparse.FileType("r"),
            help="Contains extracted data from the NLnet dashboard",
        )
        self.parser.add_argument(
            "repo",
            help="Repository where the automation should happen (e.g., ngi-nix/ngipkgs)",
        )

        # Optional
        self.parser.add_argument(
            "-n",
            "--dry",
            action="store_true",
            help="Print expected actions without making any changes",
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Print debugging information",
        )
        self.parser.add_argument(
            "-p",
            "--projects",
            help=f"Number of projects to sync (default: to {DefaultArgs.projects})",
            default=DefaultArgs.projects,
            type=int,
        )
        self.parser.add_argument(
            "--credentials",
            help=f"Directory from which GitHub credentials are loaded (default: to '{DefaultArgs.credentials}')",
            type=dir_path,
            default=DefaultArgs.credentials,
        )
        self.parser.add_argument(
            "--template",
            help=f"Directory for the project template (default: to '{DefaultArgs.template}')",
            type=dir_path,
            default=DefaultArgs.template,
        )

        self.args = self.parser.parse_args()


class DefaultArgs:
    # TODO: sync all projects by default?
    projects = 5
    credentials = "./.env"
    template = "./template"


class Deliverable(str, Enum):
    SERVICES = "services"
    EXECUTABLES = "executables"
    LIBRARIES = "libraries"
    TESTS = "tests"
    DEVENV = "devenv"


@dataclass
class GitProject:
    name: str
    branch_name: str = field(init=False)
    description: str = "\n### Websites"
    websites: Series = field(default_factory=Series)

    def __post_init__(self):
        self.branch_name = f"projects/{self.name}"

    def append_websites(self, websites: List[str]):
        self.websites = pd.concat(
            [self.websites, pd.Series(websites)], ignore_index=True
        )

    def update_description(self):
        for site in self.websites:
            self.description += f"\n- {site}"

    def clean_websites(self):
        """Remove empty values, clean up URLs and remove duplicates"""
        self.websites = cleanup_empty(self.websites)
        self.websites = cleanup_urls(self.websites)
        self.websites = self.websites.drop_duplicates()


class Subgrants(BaseModel):
    subgrants: List[Subgrant] = []

    def get_websites(self, name: str) -> List[str]:
        for s in self.subgrants:
            if name == s.name:
                return s.websites
        return []


def main():
    args = Cli().args

    load_credentials(args.credentials)

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    synced_projects = 0

    notion_file = get_notion_projects(args.notion_zip)

    if notion_file is None:
        logger.error(f"Failed to extract {args.notion_zip}")
        exit()

    projects = pd.read_csv(notion_file, usecols=["Name", "Subgrants"])
    projects["Name"] = cleanup_empty(projects["Name"])

    # Remove notion URLs from the subgrants. We need these for getting the project websites.
    projects["Subgrants"] = projects["Subgrants"].apply(
        lambda x: remove_urls(x).split(" ") if pd.notna(x) else []
    )

    projects_dict = projects.to_dict(orient="records")
    projects = [
        Project(name=item["Name"], subgrants=item["Subgrants"])
        for item in projects_dict
    ]

    try:
        with args.dashboard_file as f:
            funds = Subgrants(subgrants=ijson.items(f, "."))
    except ValidationError as e:
        logger.error(f"Failed to parse {args.dashboard_file}: {e}")
        exit()

    github = GitClient(*args.repo.split("/"))
    projects_iterator = tqdm(
        projects,
        desc="Sync Progress",
        unit="Project",
        total=args.projects,
        leave=False,
        position=0,
    )

    for project in projects_iterator:
        p = GitProject(project.name)

        for subgrant in project.subgrants:
            p.append_websites(funds.get_websites(subgrant))

        p.clean_websites()
        p.update_description()

        logger.debug(f"{p.branch_name}\n{p.description}\n")

        if not args.dry:
            # TODO: link missing artifacts to projects already in the repo
            if github.project_exists(p.name):
                logger.info(f"{p.name} already exists in repo. Skipping.")

            # Track projects
            if github.issue_exists(p.name):
                logger.info(f"{p.name} already tracked with an issue.")
            else:
                project_issue = github.create_issue(p.name, p.description)

                deliverables = list(Deliverable)
                for d in tqdm(
                    deliverables, desc=f"Deliverables for {p.name}", position=1
                ):
                    sub_issue = github.create_issue(f"{p.name}: {d.value}")
                    github.link_sub_issue(project_issue.number, sub_issue.id)

            # Add new projects to repo
            if github.pr_exists(p.name):
                logger.info(f"Pull request already open for {p.name}. Skipping.")

            if github.branch_exists(p.branch_name):
                logging.info(f"Branch already exists for {p.name}.")
            else:
                github.create_branch(p.branch_name)

            github.add_project(p.name, args.template)
            github.create_pr(p.name, p.branch_name)

        synced_projects += 1
        projects_iterator.display()

        if args.dry:
            sleep(0.5)

        if synced_projects == args.projects:
            projects_iterator.update(1)
            projects_iterator.close()
            break

    tqdm.write(f"Synced {synced_projects} Projects.")


# TODO: get status from Notion
if __name__ == "__main__":
    main()
