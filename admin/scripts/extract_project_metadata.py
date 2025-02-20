#!/usr/bin/python3

import argparse
import json
import logging
import os
import sys

import ijson
from common.models.dashboard import Fund
from common.models.notion import Overview, Subgrant
from common.utils import dir_path, get_notion_projects, remove_urls, zip_file_type
from pydantic import ValidationError
from tqdm import tqdm

# fmt: off
choices = {
    "default": lambda subgrants: {
        s.name: s.model_dump()
        for s in subgrants
    },
    "emails": lambda subgrants: sorted(
        set(s.contact.email for s in subgrants),
        key=lambda email: email.split("@")[1]
    ),
    "overview": lambda subgrants: {
        o.name: o.model_dump()
        for o in [
            Overview(name=s.name, websites=s.websites, summary=s.summary)
            for s in subgrants
        ]
    },
}
# fmt: on


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="""
            Extract medatata from the exported NLnet grant database
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
        self.parser.add_argument(
            "-p",
            "--preset",
            choices=choices.keys(),
            default="default",
            help="Output the metadata in a specific format",
        )

        self.contacts_group = self.parser.add_argument_group("Author Contacts (email)")
        self.contacts_group.add_argument(
            "author_messages_zip",
            nargs="?",
            type=zip_file_type,
            help="ZIP file containing author messages from Notion",
        )
        self.contacts_group.add_argument(
            "-s",
            "--samples",
            help="Number of new author contacts to sample (default: all)",
            type=int,
        )

        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(1)

        self.args = self.parser.parse_args()


def main():
    args = Cli().args

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    if args.preset == "emails" and args.author_messages_zip is None:
        logger.error(
            "Please provide the author messages zip file when choosing the 'emails' preset."
        )
        exit()

    subgrants = []

    logger.info("Extracting data from subgrant files")
    for input_file in os.listdir(args.input_dir):
        if not input_file.endswith(".json"):
            continue

        input_path = os.path.join(args.input_dir, input_file)

        try:
            with open(input_path, "rb") as f:
                data = ijson.items(f, "fund")
                fund = Fund(**next(data))

                for subgrant in tqdm(fund.subgrants, desc=input_file):
                    if subgrant.properties.webpage.name is None:
                        logger.warning(subgrant)
                        continue

                    subgrants.append(
                        Subgrant(
                            name=subgrant.properties.webpage.name,
                            websites=subgrant.proposal.websites.website,
                            summary=subgrant.properties.webpage.summary,
                            contact=Subgrant.Contact(
                                **subgrant.proposal.contact.model_dump()
                            ),
                        )
                    )
        except ValidationError as e:
            logger.error(e)

    content = choices[args.preset](subgrants)

    json.dump(content, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
