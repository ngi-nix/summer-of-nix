#!/usr/bin/env python3

import argparse
import json
import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import List

import pandas as pd
from pandas import Series
from pydantic import BaseModel, ValidationError

from ghkit import GitClient
from process import Result as Subgrant  # TODO: put this in a better place
from utils import cleanup_empty, cleanup_urls, remove_urls


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Read project information exported from the NLnet dashboard and Notion, and create one GitHub pull request and milestone per project, based on a template.
            """
        )

        self.parser.add_argument(
            "-n",
            "--dry",
            action="store_true",
            help="Print information without creating anything",
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
            help="Number of projects to process",
            default=1,
            type=int,
        )
        self.parser.add_argument(
            "--repo",
            help="Repository where the automation should happen",
            default="ngipkgs",
        )
        self.parser.add_argument(
            "--credentials",
            help="Directory from which GitHub credentials are loaded",
            type=dir_path,
            default="./.env",
        )
        self.parser.add_argument(
            "--template",
            help="Directory for the project template",
            type=dir_path,
            default="./template",
        )

        self.args = self.parser.parse_args()


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def load_credentials(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.read().strip()
                os.environ[filename] = content


class Deliverable(str, Enum):
    SERVICES = "services"
    EXECUTABLES = "executables"
    LIBRARIES = "libraries"
    TESTS = "tests"
    DEVENV = "development environment"


@dataclass
class Project:
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

    # TODO: make a template for this
    def update_description(self):
        if len(self.websites) > 0:
            pass

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


class NotionProject(BaseModel):
    name: str = ""
    subgrants: List[str] = []


# TODO: get status from Notion
def main():
    count = 1

    projects = pd.read_csv(input_file, usecols=["Name", "Subgrants"])
    projects["Name"] = cleanup_empty(projects["Name"])

    # Some project names have spaces in them, so we'd either need to remove
    # that in Notion or just replace them here.
    projects["Name"] = projects["Name"].apply(
        lambda x: x.replace(" ", "-") if pd.notna(x) else ""
    )

    # Remove notion URLs from the subgrants. We need these for getting the project websites.
    projects["Subgrants"] = projects["Subgrants"].apply(
        lambda x: remove_urls(x).split(" ") if pd.notna(x) else []
    )

    projects_dict = projects.to_dict(orient="records")
    projects = [
        NotionProject(name=item["Name"], subgrants=item["Subgrants"])
        for item in projects_dict
    ]

    try:
        with open(info_file, "r") as f:
            funds = Subgrants(subgrants=json.load(f))
    except ValidationError as e:
        logger.error(f"Failed to parse subgrant information from {info_file}: {e}")
        exit()

    # TODO: use env variable or argument for repo?
    github = GitClient(*os.environ["REPO"].split("/"))

    for project in projects:
        p = Project(project.name)

        for subgrant in project.subgrants:
            p.append_websites(funds.get_websites(subgrant))

        p.clean_websites()
        p.update_description()

        logger.debug(f"{p.branch_name}\n{p.description}\n")

        if not args.dry:
            # TODO: link missing artifacts to projects already in the repo
            if github.project_exists(p.name):
                logger.info(f"{p.name} already exists in repo. Skipping.")
                continue

            # Track projects
            if github.issue_exists(p.name):
                logger.info(f"{p.name} already tracked with an issue.")
            else:
                project_issue = github.create_issue(p.name, p.description)

                deliverables = list(Deliverable)
                for d in deliverables:
                    sub_issue = github.create_issue(f"{p.name} ({d.value})")
                    github.link_sub_issue(project_issue.number, sub_issue.id)

            # Add new projects to repo
            if github.pr_exists(p.name):
                logger.info(f"Pull request already open for {p.name}. Skipping.")
                continue

            if github.branch_exists(p.branch_name):
                logging.info(f"Branch already exists for {p.name}.")
            else:
                github.create_branch(p.branch_name)

            github.add_project(p.name, args.template)
            github.create_pr(p.name, p.branch_name)

        if count == args.projects:
            break

        count += 1


if __name__ == "__main__":
    args = Cli().args

    load_credentials(args.credentials)

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)

    input_file = "./projects.csv"
    info_file = "./info.json"

    main()
