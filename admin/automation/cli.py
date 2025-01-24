import argparse


class Cli:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
            "-d",
            "--dry_run",
            action="store_true",
            help="Print information without creating anything",
        )
        self.parser.add_argument(
            "-n", "--number", help="Number of projects to process", default=1, type=int
        )
        self.parser.add_argument(
            "--repo",
            help="Repository where the automation should happen",
            default="ngipkgs",
        )
        self.parser.add_argument(
            "--template",
            help="Location for the project template file in Nix",
            default="./template.nix",
        )

        self.args = self.parser.parse_args()
