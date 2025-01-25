# Description

Scripts to automatically open PRs for projects and track them in milestones.

# Usage

Currently, the scripts require passing manual data from Notion and the NLnet dashboard.
In the future, this step will be automatically done by connecting to the data sources directly.

## Setup

Connecting with the GitHub API requires an authentication token.
Create a [fine-grained token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) with the following permissions:

- Pull Requests: Read & write
- Contents: Read & write

After generating the token, put it in a `.env` file in this directory in the following format:

```
GH_TOKEN="<TOKEN>"
```

## Getting Data

### NLnet Dashboard

Run the extraction script on a directory containing the JSON files exported from the NLnet dashboard:

```sh
extract-project-data-from-nlnet ./directory >> projects.json
```

The result is a JSON file that contains relevant information for each subgrant, which will later be used to populate the milestones.

#### Notion

Get the project list from Notion:

- Navigate to the [Projects list](https://www.notion.so/nixos-foundation/15759d49e1be808186e5dc8c2c600ba8?v=9e8141539d9c41ad98ab2368b12d030f)
- Make sure that the `Subgrants` field is in the view
- Click on the top-right menu and export as a csv

Put the exported file in this directory under the name `projects.csv`.


Run

```sh
create-prs --help
```

and follow the instructions.
