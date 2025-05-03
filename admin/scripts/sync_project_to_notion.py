import argparse
import sys

import pandas as pd
from common.utils import cleanup_empty, get_notion_projects, zip_file_type
from pandas import DataFrame


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Sync subgrants from the NLnet dashboard to Notion
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
    notion_file = get_notion_projects(args.notion_zip)

    if notion_file is None:
        print(f"Failed to extract {args.notion_zip}")
        exit()

    reference: DataFrame = pd.read_csv(notion_file, usecols=notion_fields)
    reference["Subgrant ID"] = cleanup_empty(reference["Subgrant ID"])

    subgrants = pd.read_csv(args.dashboard_file, usecols=notion_fields)
    subgrants["Name"] = subgrants["Name"].sort_values().drop_duplicates()

    # Remove entries already in Notion
    subgrants = subgrants[~subgrants["Subgrant ID"].isin(reference["Subgrant ID"])]

    subgrants.to_csv(sys.stdout, encoding="utf-8", index=False)
