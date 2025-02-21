#!/usr/bin/python3

import argparse
import json
import sys

import ijson
from common.models import Form, Project


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

    with args.form_file as f:
        data = ijson.items(f, "")
        form = Form(**next(data))

    projects = [
        Project(
            name=r.project_name,
            author=Project.Author(author_name=r.author_name, role=r.author_role),
            contributors=r.contributors,
            build_system=Project.CI_CD(
                build_failure_duration=r.build_failure_duration,
                dependency_update=r.has_dependency_update,
            ),
        )
        for r in form.responses
    ]

    json.dump([p.model_dump() for p in projects], sys.stdout, indent=2)


if __name__ == "__main__":
    main()
