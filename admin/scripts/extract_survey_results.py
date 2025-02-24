#!/usr/bin/python3

import argparse
import json
import logging
import sys

import ijson
from common.models import Form, Project, project_from_response


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="",
        )

        self.parser.add_argument(
            "form_file",
            type=argparse.FileType("r"),
            help="",
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


def main():
    args = Cli().args

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    with args.form_file as f:
        data = ijson.items(f, "")
        form = Form(**next(data))

    projects: list[Project] = []

    for r in form.responses:
        project, msg = project_from_response(r)

        if project is None:
            logger.error(
                f'"{r.project_name}" has an invalid field: "{msg}". Skipping project entry.'
            )
            continue

        projects.append(project)

    json.dump([p.model_dump() for p in projects], sys.stdout, indent=2)


if __name__ == "__main__":
    main()
