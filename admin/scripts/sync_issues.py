#!/bin/python

import argparse
import json
import logging
import sys
import textwrap
from dataclasses import dataclass, field
from time import sleep
from typing import List

import pandas as pd
from common.ghkit import GitClient
from common.models.notion import Subgrant
from common.utils import (
    cleanup_empty,
    cleanup_urls,
    dir_path,
    get_notion_projects,
    load_credentials,
    remove_urls,
    zip_file_type,
)
from pandas import Series
from pydantic import BaseModel, ValidationError
from tqdm import tqdm


@dataclass
class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Read the project list and metadata files and create one GitHub issue per project.
            """
        )

        # Positional
        self.parser.add_argument(
            "projects_list_file",
            type=zip_file_type,
            help="ZIP file containing the exported list of projects from Notion",
        )
        self.parser.add_argument(
            "metadata_file",
            type=argparse.FileType("r"),
            help="Contains extracted project metadata from the NLnet dashboard in JSON format",
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
            help="Number of projects to sync (default: all projects)",
            type=int,
        )
        self.parser.add_argument(
            "--credentials",
            help="Directory from which GitHub credentials are loaded (default: %(default)s)",
            type=dir_path,
            default="./.env",
        )

        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(1)

        self.args = self.parser.parse_args()


@dataclass
class GitProject:
    @dataclass
    class Description(str):
        websites: str = ""
        nlnet_pages: str = ""
        source_code: str = ""

        def __str__(self):
            return textwrap.dedent(f"""
            ### NLnet Projects
            {self.nlnet_pages}

            ### Websites
            {self.websites}
            """)

        def __repr__(self):
            return self.__str__()

    name: str
    subgrants: list[str] = field(default_factory=list)

    branch_name: str = field(init=False)
    description: Description = field(default_factory=Description)
    websites: Series = field(default_factory=Series)

    def __post_init__(self):
        self.branch_name = f"projects/{self.name}"

    def append_websites(self, websites: List[str]):
        self.websites = pd.concat(
            [self.websites, pd.Series(websites)], ignore_index=True
        )

    def update_nlnet_links(self, subgrants: list[str]):
        self.description.nlnet_pages = "\n".join(
            f"- https://nlnet.nl/project/{s}" for s in subgrants
        )

    def update_description(self):
        self.clean_websites()
        for site in self.websites:
            self.description.websites += f"\n- {site}"

    def clean_websites(self):
        """Remove empty values, clean up URLs and remove duplicates"""
        self.websites = cleanup_empty(self.websites)
        self.websites = cleanup_urls(self.websites)
        self.websites = self.websites.drop_duplicates()


class Subgrants(BaseModel):
    subgrants: dict[str, Subgrant]

    def get_websites(self, name: str) -> list[str]:
        if name in self.subgrants:
            return self.subgrants[name].websites
        return []


def main():
    args = Cli().args

    load_credentials(args.credentials)

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    synced_projects = 0

    notion_file = get_notion_projects(args.projects_list_file)

    if notion_file is None:
        logger.error(f"Failed to extract {args.projects_list_file}")
        exit()

    projects = pd.read_csv(notion_file, usecols=["Name", "Subgrants"])
    projects["Name"] = cleanup_empty(projects["Name"])

    # Remove notion URLs references from the Subgrants column
    projects["Subgrants"] = projects["Subgrants"].apply(
        lambda x: remove_urls(x).split(" ") if pd.notna(x) else []
    )

    projects_dict = projects.to_dict(orient="records")
    projects = [
        GitProject(name=item["Name"], subgrants=item["Subgrants"])
        for item in projects_dict
    ]

    try:
        with args.metadata_file as f:
            funds = Subgrants(subgrants=json.load(f))
    except ValidationError as e:
        logger.error(f"Failed to parse {args.metadata_file}: {e}")
        exit()

    gh = GitClient(*args.repo.split("/")) if not args.dry else None

    total_projects = args.projects if args.projects != 0 else len(projects)

    projects_iter = tqdm(
        projects,
        desc="Sync Progress",
        unit="Project",
        total=total_projects,
        position=0,
    )

    for project in projects_iter:
        p = GitProject(project.name)

        for subgrant in project.subgrants:
            p.append_websites(funds.get_websites(subgrant))

        p.update_nlnet_links(project.subgrants)
        p.update_description()

        logger.debug(f"{p.branch_name}\n{p.description}\n")

        if gh is not None:
            gh.create_issue(p.name, p.description)

        synced_projects += 1
        projects_iter.display()

        if args.dry:
            sleep(0.5)

        if synced_projects == args.projects:
            projects_iter.update(1)
            projects_iter.close()
            break


if __name__ == "__main__":
    main()
