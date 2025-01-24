#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p jaq "python3.withPackages(ps: with ps; [ pandas pygithub python-dotenv ])"

"""
Extract useful information from processed grant files
"""

import os
import subprocess

import pandas as pd

input = "./funds"
output = "./info.json"


if __name__ == "__main__":
    subprocess.call(["bash", "./process.sh"])

    columns = ["Name", "Websites", "Summary"]
    subgrants = pd.DataFrame(columns=columns)

    for file in os.listdir(input):
        file_path = os.path.join(input, file)

        if os.path.isfile(file_path) and file.endswith("-processed.json"):
            df = pd.read_json(file_path)[columns]
            subgrants = pd.concat([subgrants, df])

    subgrants.drop_duplicates(subset="Name", inplace=True)
    subgrants.set_index("Name", inplace=True)
    subgrants.to_json(output, orient="index", indent=2)
