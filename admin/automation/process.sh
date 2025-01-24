#!/usr/bin/env nix-shell
#!nix-shell -i bash -p bash jaq

INPUT_DIR="${1:-./funds}"
OUT_DIR="${2:-$INPUT_DIR}"

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: '$INPUT_DIR' does not exist or is not a directory."
    exit 1
fi

if [ ! -d "$OUT_DIR" ]; then
    mkdir -p "$OUT_DIR"
fi

for input in "$INPUT_DIR/"*.json; do
    filename=$(basename "$input")
    output="$OUT_DIR/${filename%.json}-processed.json"

    if [[ "$filename" == *-processed.json ]]; then
        continue
    fi

    jaq '[ .fund.proposals[] |
        {
            "Name": .properties.webpage.sitename,
            "Websites": .proposal.websites.website,
            "Summary": .properties.webpage.summary,
        }
    ]' "$input" >"$output"
done
