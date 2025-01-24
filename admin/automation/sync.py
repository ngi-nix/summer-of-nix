#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: with ps; [ pandas pygithub python-dotenv ])"

import pandas as pd
from dotenv import load_dotenv

from cli import Cli
from gh import GH
from utils import cleanup_empty, cleanup_urls, remove_urls

args = Cli().args

input = "./projects.csv"

count = 1


if __name__ == "__main__":
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

    # WARN: You need to add `GH_TOKEN=<your token>` in a .env file
    load_dotenv()

    gh = GH(args.repo)

    for i, project in projects.iterrows():
        name = project.name

        if gh.project_exists(name):
            print(f"{name} already exists in repo. Skipping.")
            continue

        if gh.pr_exists(name):
            print(f"Pull request already open for {name}. Skipping.")
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
        else:
            print(description)

        if count == args.number:
            break

        count += 1

    gh.close()
