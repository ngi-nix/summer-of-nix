import argparse
import shutil
import sys

import pandas as pd
from common.utils import cleanup_empty, get_notion_projects, zip_file_type
from pandas import DataFrame


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Sync subgrants from the NLnet dashboard to Notion

            Usage Instructions:

            - Open subgrants page: https://www.notion.so/nixos-foundation/0bea42f64e3d4780ab5ed918229ac693?v=541d01bba2b34142a28f3d8c3682e6f5
            - Click the top right menu
            - Export database (keep defaults)
            - Download the zip file and rename it to `subgrants.zip`
            - Download all funds from the dashboard as `json` (see `scripts/README.md`)
            - Put them all in a single directory (e.g. `funds/`) 
            - Go to `admin` directory of the `summer-of-nix` repo and run `nix-shell`
            - Put `subgrants.zip` and `funds/` from the previous steps here
            - Run `python scripts/extract_project_metadata.py -f csv ./funds > info.csv`
            - Run `python sync_project_to_notion.py ./subgrants.zip ./info.csv > import.csv`
            """
        )
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
            "-d",
            "--debug",
            action="store_true",
            help="Print debugging information",
        )

        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(1)

        self.args = self.parser.parse_args()


if __name__ == "__main__":
    args = Cli().args

    notion_fields = ["Name", "Subgrant ID", "Fund"]
    notion_projects = get_notion_projects(args.notion_zip)

    if notion_projects is None:
        print(f"Failed to extract {args.notion_zip}")
        exit()

    notion_file, tmp_dir = notion_projects

    reference: DataFrame = pd.read_csv(notion_file, usecols=notion_fields)
    reference["Name"] = cleanup_empty(reference["Name"])

    subgrants = pd.read_csv(args.dashboard_file, usecols=notion_fields)
    subgrants["Name"] = subgrants["Name"].sort_values().drop_duplicates()

    # Remove entries already in Notion
    subgrants = subgrants[~subgrants["Name"].isin(reference["Name"])]

    subgrants.to_csv(sys.stdout, encoding="utf-8", index=False)

    missing_notion_ids = reference[reference["Subgrant ID"].isna()]

    if not missing_notion_ids.empty:
        print("\n--- Notion Subgrants with missing IDs ---\n", file=sys.stderr)
        for name in missing_notion_ids["Name"]:
            print(f"- {name}", file=sys.stderr)
        print("\n------------------------------------\n", file=sys.stderr)

    shutil.rmtree(tmp_dir, ignore_errors=True)
