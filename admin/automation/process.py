#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p jaq "python3.withPackages(ps: with ps; [ pydantic ])"

import argparse
import json
import logging
import os
from typing import List, Optional

from pydantic import BaseModel, ValidationError


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Extract useful information from processed grant files
            """
        )
        self.parser.add_argument(
            "-i",
            "--input",
            type=dir_path,
            help="Input directory containing grant files",
            default="./funds",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            # TODO: better message?
            help="Output file",
            default="./info.json",
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Print debugging information",
        )
        self.args = self.parser.parse_args()


class Proposal(BaseModel):
    Name: Optional[str]
    Websites: List[str]
    Summary: Optional[str]


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def map_fund_data(input_file: str, all_proposals: List[Proposal]):
    with open(input_file, "r") as f:
        data = json.load(f)

    proposals = data.get("fund", {}).get("proposals", [])

    for p in proposals:
        name = p.get("properties", {}).get("webpage", {}).get("sitename")
        websites = p.get("proposal", {}).get("websites", {}).get("website", [])
        summary = p.get("properties", {}).get("webpage", {}).get("summary")

        proposal_data = {"Name": name, "Websites": websites, "Summary": summary}

        try:
            if name is None:
                logging.warning(f"Skipping entry due to null name: {proposal_data}")
                continue
            all_proposals.append(Proposal(**proposal_data))
        except ValidationError as e:
            logger.error(f"Invalid data for proposal: {proposal_data}. Error: {e}")


def main(input_dir: str, output_file: str):
    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' does not exist or is not a directory.")
        exit(1)

    all_proposals = []

    for input_file in os.listdir(input_dir):
        if input_file.endswith(".json"):
            input_path = os.path.join(input_dir, input_file)
            map_fund_data(input_path, all_proposals)

    # Write all processed proposals to a single output file
    with open(output_file, "w") as f:
        json.dump([proposal.dict() for proposal in all_proposals], f, indent=4)


if __name__ == "__main__":
    args = Cli().args

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)

    main(args.input, args.output)
