#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys

from models_dashboard import Fund
from models_notion import Subgrant
from pydantic import ValidationError
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
                    Subgrant(
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
