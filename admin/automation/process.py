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


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


class Websites(BaseModel):
    website: List[str]


class Webpage(BaseModel):
    sitename: str = ""
    summary: str


class PropertiesField(BaseModel):
    webpage: Webpage


class ProposalField(BaseModel):
    websites: Websites


class Proposal(BaseModel):
    properties: PropertiesField
    proposal: ProposalField


class Fund(BaseModel):
    proposals: List[Proposal]


class Result(BaseModel):
    Name: str
    Websites: List[str]
    Summary: str


def main(input_dir: str, output_file: str):
    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' does not exist or is not a directory.")
        exit(1)

    proposals = []

    for input_file in os.listdir(input_dir):
        if input_file.endswith(".json"):
            input_path = os.path.join(input_dir, input_file)

            with open(input_path, "r") as f:
                data = json.load(f)

            try:
                fund = Fund(**data["fund"])
                for proposal in fund.proposals:
                    name = proposal.properties.webpage.sitename
                    websites = proposal.proposal.websites.website
                    summary = proposal.properties.webpage.summary

                    if name == "":
                        logger.debug(proposal)
                        continue

                    proposals.append(
                        Result(
                            Name=name,
                            Websites=websites,
                            Summary=summary,
                        )
                    )
            except ValidationError as e:
                logger.error(e)

    # Write all processed proposals to a single output file
    with open(output_file, "w") as f:
        json.dump([proposal.dict() for proposal in proposals], f, indent=4)


if __name__ == "__main__":
    args = Cli().args

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    main(args.input, args.output)
