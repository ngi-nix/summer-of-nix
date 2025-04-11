#!/bin/env bash

true <<EOF
Script that creates migration issues for each project, given a list of project names.

Note that each project name should be stored in a newline.

USAGE:

./create-migration-issues.sh <INPUT_FILE> <REPO>
EOF

DRY_RUN=true
INPUT_FILE="${1:-./list.txt}"
REPO="${2:-ngi-nix/ngipkgs}"

fence='```'

while read -r project; do
    TITLE="Migrate \`$project\` from projects-old to projects"
    BODY=$(cat ./body.md)
    BODY=$(
        cat <<-EOF
	## Instructions

	1. Copy the project template to the projects directory:

	   ${fence}
	   cp -r templates/project projects/$project
	   ${fence}

	1. Search for \`NGI Project: $project\` in the [Ngipkgs issues](https://github.com/ngi-nix/ngipkgs/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22NGI%20Project%22) page.
	   If a page with that name exists, use the information available there in the next step.

	1. Open the new project file and fill in the missing data, using the information in \`projects-old/$project/default.nix\`.

	   ${fence}
	   \$EDITOR projects/$project/default.nix
	   ${fence}

	   **Note:** the code structure of \`projects-old\` is different from \`projects\`, so copying information without adhering to that structure will lead to test errors.

	1. Check that the code is valid by running the test locally:

	   ${fence}
	   # examples
	   $ nix build .#checks.x86_64-linux.projects/$project/nixos/examples/<example_name>

	   # tests
	   $ nix build .#checks.x86_64-linux.projects/$project/nixos/tests/<test_name>
	   ${fence}

	1. Delete the \`projects-old/$project\` directory
	1. Run the Nix code formatter with \`nix fmt\`
	1. Commit your changes and [create a new PR](#how-to-create-pull-requests-to-ngipkgs)
	EOF
    )

    if $DRY_RUN; then
        >&2 echo "==="
        >&2 echo "${TITLE}"
        >&2 echo "---"
        >&2 echo "${BODY}"
    else
        gh issue create \
            --repo "$REPO" \
            --title "$TITLE" \
            --body "$BODY" \
            --label "good first issue"
    fi
done <"$INPUT_FILE"
