# Description

Scripts to automatically open PRs for projects and track them in issues.

# Setup

## Credentials

Create a [fine-grained token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) with the following permissions:

- Contents: Read & write
- Issues: Read & write
- Pull Requests: Read & write

Put the token in a file with the name `GH_TOKEN` in your crendentials directory. Example:

```sh
$ cat .env/GH_TOKEN
<TOKEN>
```

In the same directory, put the repository you'd like to sync with in a `REPO` file. Example:

```sh
$ cat .env/REPO
ngi-nix/ngipkgs
```

## NLnet Dashboard

Activate the development environment:

```sh
nix-shell
```

Run the extraction script on a directory containing the JSON files exported from the NLnet dashboard:

```sh
extract-project-data ./directory >>projects.json
```

## Notion

Get the project list from Notion:

- Navigate to the [Projects list](https://www.notion.so/nixos-foundation/15759d49e1be808186e5dc8c2c600ba8?v=9e8141539d9c41ad98ab2368b12d030f)
- Make sure that the `Subgrants` field is in the view
- Click on the top-right menu and export as a csv
- Export the file in your filesystem

# Usage

With the development environment active, run:

```sh
sync-projects --help
```

and follow the instructions.
