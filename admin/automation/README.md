## Description

Scripts to automatically open PRs for projects and track them in milestones.

## Usage

Currently, the scripts require manual data from Notion and the dashboard.
In the future, this step will be automatically done by connecting to them
through directly.

### Setup

#### GitHub authentication

Connecting with the GitHub API requires an authentication token. Create a [fine-grained token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) with the following permissions:

- Pull Requests: Read & write
- Contents: Read & write

After generating the token, put it in a `.env` file in this directory in the
following format:

```
GH_TOKEN="<TOKEN>"
```

### Getting Data

#### Dashboard

Execute the `process.py` script on a directory containing the json files for
the dashboard.

```sh
./process.py
```

The result is a json that contains the name and websites for subgrants, which
will later be used to populate the milestones.

#### Notion

Get the project list from Notion:

- Navigate to the [Projects list](https://www.notion.so/nixos-foundation/15759d49e1be808186e5dc8c2c600ba8?v=9e8141539d9c41ad98ab2368b12d030f)
- Make sure that the `Subgrants` field is in the view
- Click on the top-right menu and export as a csv

Put the exported file in this directory under the name `projects.csv`.

### Creating Automatic PRs

Execute the main script with the data files as input, specifying the number of
projects to sync with `-n`:

```sh
./sync.py -n 10
```

To see which projects will be synced and how the milestone descriptions will
look like without running anything, use:

```sh
./sync.py -n 10 --dry_run
```
