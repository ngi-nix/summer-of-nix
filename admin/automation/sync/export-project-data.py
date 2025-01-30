#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
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


class Fund(BaseModel):
    @dataclass
    class Subgrant(BaseModel):
        @dataclass
        class Properties(BaseModel):
            @dataclass
            class Webpage(BaseModel):
                name: Optional[str] = Field(
                    default=None,
                    alias="sitename",
                    description="Symbolic name for the subgrant, as shown under https://nlnet.nl/project",
                    examples=["GNUnet-CONG"],
                )
                summary: str

            webpage: Webpage

        @dataclass
        class Proposal(BaseModel):
            @dataclass
            class Websites(BaseModel):
                website: List[str]

            @dataclass
            class Contact(BaseModel):
                name: str
                email: str
                organisationName: str

            websites: Websites
            contact: Contact

        properties: Properties
        proposal: Proposal

    subgrants: List[Subgrant] = Field(
        alias="proposals",
    )


class MappedSubgrant(BaseModel):
    name: Optional[str] = Field(default=None)
    websites: List[str]
    summary: str
    contact: Fund.Subgrant.Proposal.Contact


if __name__ == "__main__":
    args = Cli().args

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    subgrants = []

    for input_file in os.listdir(args.input_dir):
        if not input_file.endswith(".json"):
            continue

        input_path = os.path.join(args.input_dir, input_file)

        with open(input_path, "r") as f:
            data = json.load(f)

        try:
            fund = Fund(**data["fund"])

            for subgrant in fund.subgrants:
                if subgrant.properties.webpage.name is None:
                    logger.warning(subgrant)
                    continue

                subgrants.append(
                    MappedSubgrant(
                        name=subgrant.properties.webpage.name,
                        websites=subgrant.proposal.websites.website,
                        summary=subgrant.properties.webpage.summary,
                        contact=subgrant.proposal.contact,
                    )
                )
        except ValidationError as e:
            logger.error(e)

    content = [s.model_dump() for s in subgrants]
    json.dump(content, sys.stdout, indent=2)
