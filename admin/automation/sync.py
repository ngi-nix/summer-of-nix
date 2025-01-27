#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: with ps; [ pandas pygithub ])"

import argparse
import logging
import os
from dataclasses import dataclass, field

import pandas as pd

from gh import GH
from utils import cleanup_empty, cleanup_series, remove_urls


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
            help="Location for the project template file",
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


@dataclass
class Project:
    name: str
    branch_name: str = field(init=False)
    description: str = ""
    websites: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.branch_name = f"projects/{self.name}"


args = Cli().args


# Debugging
logger = logging.getLogger(__name__)
logging_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=logging_level)

input = "./projects.csv"


def main():
    count = 1

    projects = pd.read_csv(input, usecols=["Name", "Subgrants"])
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

    # Contains websites
    funds = pd.read_json("./info.json")

    load_credentials(args.credentials)

    with GH(args.repo) as gh:
        github = gh

    for _i, project in projects.iterrows():
        p = Project(str(project["Name"]))

        if github.project_exists(p.name):
            logger.info(f"{p.name} already exists in repo. Skipping.")
            continue

        if github.pr_exists(p.name):
            logger.info(f"Pull request already open for {p.name}. Skipping.")
            continue

        for subgrant in project["Subgrants"]:
            p.websites += funds.get(subgrant, {}).get("Websites", [])

        websites = pd.Series(p.websites)
        websites = cleanup_series(websites)

        if len(websites) > 0:
            if p.description == "":
                p.description = "\n### Websites"

            for site in websites:
                p.description += f"\n- {site}"

        logger.debug(f"{p.branch_name}\n{p.description}\n")

        # TODO: refactor?
        if not args.dry:
            if github.branch_exists(p.branch_name):
                # TODO: if branch exists, perhaps update its contents?
                logging.info(f"Branch already exists for {p.name}.")
            else:
                github.create_branch(p.branch_name)
                github.add_project(p.name, args.template)

            # TODO: automatically delete branch when PRs are closed?
            pr = github.create_pr(p.name, p.branch_name)

            if not github.milestone_exists(p.name):
                github.create_milestone(p.name, [pr], p.description)

        if count == args.projects:
            break

        count += 1


if __name__ == "__main__":
    main()
