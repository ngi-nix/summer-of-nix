# Description

Automatically open issues for NLnet projects containing useful project metadata.

# Setup

First, make sure that you're inside the development environment:

```sh
nix-shell
```

If you have [direnv](https://github.com/nix-community/nix-direnv) installed, you can also automatically do this when you enter the directory by executing:

```sh
direnv allow
```

## Credentials

Create a [fine-grained token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) with the following permissions:

- Issues: Read & write

Store the token in a `.env/GH_TOKEN` file. For example:

```sh
$ cat .env/GH_TOKEN
<TOKEN>
```

## NLnet Dashboard

Download projects metadata from NLnet dashboard:

- Go the the [NLnet dashboard](https://dashboard.nlnet.nl) and enter your credentials
- Go to each grant page, append `?json=true` to the URL, and download the file
- Put all downloaded files in a single directory

Then, to extract the data, run:

```sh
extract-project-metadata ./directory >>metadata.json
```

## Notion

Get the project list from Notion:

- Navigate to the [Projects list](https://www.notion.so/nixos-foundation/15759d49e1be808186e5dc8c2c600ba8?v=9e8141539d9c41ad98ab2368b12d030f) page
- If you can't access the page, you should request permissions
- In the database table, make sure that the `Subgrants` field is in the view
- Click on the top-right menu and export as a csv, choosing the default options
- Save the ZIP file to your filesystem

# Usage

With the development environment active, run:

```sh
sync-issues --help
```

and follow the instructions.
