#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: with ps; [ pandas pygithub ])"

import argparse
import logging
import os

import pandas as pd

from gh import GH
from utils import cleanup_empty, cleanup_urls, remove_urls


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Read project information exported from the NLnet dashboard and Notion, and create one GitHub pull request and milestone per project, based on a template.
            """
        )

        self.parser.add_argument(
            "-d",
            "--dry_run",
            action="store_true",
            help="Print information without creating anything",
        )
        self.parser.add_argument(
            "-n", "--number", help="Number of projects to process", default=1, type=int
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


args = Cli().args


logger = logging.getLogger(__name__)
input = "./projects.csv"

logging.basicConfig()
logger.setLevel(logging.DEBUG)


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

    projects.set_index("Name", inplace=True)

    # Contains websites
    funds = pd.read_json("./info.json")

    load_credentials(args.credentials)

    gh = GH(args.repo)

    for _i, project in projects.iterrows():
        name = project.name

        if gh.project_exists(name):
            logger.info(f"{name} already exists in repo. Skipping.")
            continue

        if gh.pr_exists(name):
            logger.info(f"Pull request already open for {name}. Skipping.")
            continue

        # Preparing contents
        branch_name = f"projects/{name}"
        websites = []

        for subgrant in project["Subgrants"]:
            websites += funds.get(subgrant, {}).get("Websites", [])

        # TODO: refactor?
        websites = pd.Series(websites)
        websites = cleanup_urls(websites)
        websites = cleanup_empty(websites)
        websites.drop_duplicates()

        description = ""
        if len(websites) > 0:
            description += "\n### Websites"
            for site in websites:
                description += f"\n- {site}"

        logger.debug(f"\n{branch_name}\n{description}\n")

        # TODO: refactor?
        if not args.dry_run:
            if gh.branch_exists(branch_name):
                # TODO: if branch exists, perhaps update its contents?
                print(f"Branch already exists for {name}.")
            else:
                gh.create_branch(branch_name)
                gh.add_project(name, args.template)

            # TODO: automatically delete branch when PRs are closed?
            pr = gh.create_pr(name, branch_name)

            if not gh.milestone_exists(name):
                gh.create_milestone(name, [pr], description)

        if count == args.number:
            break

        count += 1

    gh.close()


if __name__ == "__main__":
    main()
