#!/usr/bin/python3

import argparse
import json
import logging
import os
import random
import sys
import textwrap
from contextlib import contextmanager

import ijson
import pandas as pd
import questionary
from common.models.dashboard import Fund
from common.models.notion import AuthorMessages, Overview, Subgrant
from common.utils import dir_path, get_notion_projects, remove_urls, zip_file_type
from pydantic import ValidationError
from tqdm import tqdm

# fmt: off
choices = {
    "default": lambda inputs: {
        s.name: s.model_dump()
        for s in inputs["subgrants"]
    },
    "emails": lambda inputs: get_new_contacts_for_message(**inputs),
    "overview": lambda inputs: {
        o.name: o.model_dump()
        for o in [
            Overview(name=s.name, websites=s.websites, summary=s.summary)
            for s in inputs["subgrants"]
        ]
    },
}
# fmt: on


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description=textwrap.dedent(f"""\
            Extract medatata from the exported NLnet grant database

            Examples:
            # Extract metadata
            {sys.argv[0]} <NLNET-METADATA-DIRECTORY> > metadata.json

            # Get the list of project author emails for a certain message
            {sys.argv[0]} <NLNET-METADATA-DIRECTORY> <MESSAGES-ZIP> -p emails > emails.csv

            ---

            """),
            formatter_class=argparse.RawTextHelpFormatter,
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
            "messages_zip",
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


@contextmanager
def redirect_stdout(tmp_stream):
    """Temporarily redirect sys.stdout to a different output stream"""
    original_stdout = sys.stdout
    sys.stdout = tmp_stream
    try:
        yield
    finally:
        sys.stdout = original_stdout


def get_new_contacts_for_message(
    logger: logging.Logger, args: argparse.Namespace, subgrants: list[Subgrant]
):
    """
    Prompts users to choose a message, then determines which NGI project authors
    have not been contacted for that message, yet
    """
    messages = get_notion_projects(args.messages_zip)

    if messages is None:
        logger.error(f"Failed to extract {args.messages_zip}")
        exit()

    messages = pd.read_csv(messages, usecols=["Name", "Already contacted"])
    messages["Already contacted"] = messages["Already contacted"].apply(
        lambda x: remove_urls(x) if pd.notna(x) else ""
    )
    messages = {
        m["Name"]: AuthorMessages(message=m["Name"], contacted=m["Already contacted"])
        for m in messages.to_dict(orient="records")
    }

    # Prompt users through stderr since stdout is already used for the result
    with redirect_stdout(sys.stderr):
        response: str | None = questionary.select(
            "What email message do you need?",
            choices=[n.message for n in messages.values()],
        ).ask()

    if response is None:
        exit()

    new_contacts: list[str] = []
    for c in subgrants:
        if c.contact.name in messages[response].contacted:
            continue
        new_contacts.append(f'"{c.contact.name}","<{c.contact.email}>"')
    new_contacts = sorted(set(new_contacts))

    if args.samples is not None:
        new_contacts = random.sample(new_contacts, args.samples)

    print("Name,Email")
    for c in new_contacts:
        print(c)
    exit()


def main():
    args = Cli().args

    logger = logging.getLogger(__name__)
    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    if args.preset == "emails" and args.messages_zip is None:
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

    content = choices[args.preset](
        {"logger": logger, "args": args, "subgrants": subgrants}
    )

    json.dump(content, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
