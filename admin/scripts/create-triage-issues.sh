#!/bin/env bash

true <<EOF
Script that creates issues to triage ngipkgs projects.

The script checks whether the project has already been triaged before or if a
task to triage it has already been opened.

USAGE:

./create-migration-issues.sh <NGIPKGS> <REPO>
EOF

NGIPKGS="${1:-$HOME/ngipkgs}"
REPO="${2:-ngi-nix/ngipkgs}"

DIRS=("$NGIPKGS/projects" "$NGIPKGS/projects-old")
DRY_RUN=true

# triaged projects
output_projects=$(gh issue list --repo "ngi-nix/ngipkgs" --limit 1000 --label "NGI Project" --search "NGI Project: " --json title)
# triage tasks
output_tasks=$(gh issue list --repo "ngi-nix/ngipkgs" --limit 1000 --label "good first issue" --search "Triage data for: " --json title)

# get lists
gh_projects=$(echo "$output_projects" | jq -r '.[].title | select(test("NGI Project: ")) | sub("NGI Project: "; "") | ltrimstr(" ")')
gh_tasks=$(echo "$output_tasks" | jq -r '.[].title | select(test("Triage data for ")) | sub("Triage data for "; "") | ltrimstr(" ") | gsub("`"; "")')

repo_projects=()

create_triage_issue() {
    TITLE="Triage data for \`$1\`"
    BODY=$(
        cat <<-EOF
	 Follow the instructions for [triaging an NGI project](https://github.com/ngi-nix/ngipkgs/blob/main/CONTRIBUTING.md#triaging-an-ngi-project) and collect some relevant information about this project, which will later be used to expose its packaging state.
	EOF
    )

    echo "Creating triaging issue for '$project' in $REPO"
    if $DRY_RUN; then
        >&2 echo "==="
        >&2 echo "${TITLE}"
        >&2 echo "---"
        >&2 echo "${BODY}"
        >&2 echo "==="
    else
        gh issue create \
            --repo "$REPO" \
            --title "$TITLE" \
            --body "$BODY" \
            --label "good first issue"
    fi
}

# get all projects in the repo
for dir in "${DIRS[@]}"; do
    for project in "$dir"/*; do
        if [ -d "$project" ]; then
            repo_projects+=("$(basename "$project")")
        fi
    done
done

true >./not-triaged.txt # empty file
for project in "${repo_projects[@]}"; do
    exists=false
    for name in $gh_projects; do
        if [[ "$name" == "$project" ]]; then
            # project already triaged
            exists=true
            break
        fi
    done
    for name in $gh_tasks; do
        if [[ "$name" == "$project" ]]; then
            # task already created for project
            exists=true
            break
        fi
    done
    if ! $exists; then
        if $DRY_RUN; then
            echo "Project '$project' is not triaged."
            echo "$project" >>./not-triaged.txt
        fi
        create_triage_issue "$project"
    fi
done

if $DRY_RUN; then
    # sort output in-place, uppercase first
    LC_COLLATE=C sort -o ./not-triaged.txt{,}
fi
