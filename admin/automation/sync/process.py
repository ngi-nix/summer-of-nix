#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError
from utils import dir_path


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Extract useful information from processed grant files
            """
        )
        self.parser.add_argument(
            "input_dir",
            type=dir_path,
            help="Input directory, containing grant files",
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Print debugging information",
        )
        self.args = self.parser.parse_args()


class Contact(BaseModel):
    name: str
    email: str
    organisationName: str


class Websites(BaseModel):
    website: List[str]


class Webpage(BaseModel):
    sitename: Optional[str] = Field(default=None)
    summary: str


class PropertiesField(BaseModel):
    webpage: Webpage


class ProposalField(BaseModel):
    websites: Websites
    contact: Contact


class Proposal(BaseModel):
    properties: PropertiesField
    proposal: ProposalField


class Fund(BaseModel):
    proposals: List[Proposal]


class Result(BaseModel):
    name: Optional[str] = Field(default=None)
    websites: List[str]
    summary: str
    contact: Contact


if __name__ == "__main__":
    args = Cli().args

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    proposals = []

    for input_file in os.listdir(args.input_dir):
        if not input_file.endswith(".json"):
            continue

        input_path = os.path.join(args.input_dir, input_file)

        with open(input_path, "r") as f:
            data = json.load(f)

        try:
            fund = Fund(**data["fund"])

            # TODO: improve
            for proposal in fund.proposals:
                if proposal.properties.webpage.sitename is None:
                    logger.debug(proposal)
                    continue

                proposals.append(
                    Result(
                        name=proposal.properties.webpage.sitename,
                        websites=proposal.proposal.websites.website,
                        summary=proposal.properties.webpage.summary,
                        contact=proposal.proposal.contact,
                    )
                )
        except ValidationError as e:
            logger.error(e)

    content = [proposal.model_dump() for proposal in proposals]
    json.dump(content, sys.stdout, indent=2)
