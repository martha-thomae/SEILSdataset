#!/bin/bash

SOURCE="./partitioned"
DEST="./staffEncodingsCleaned"

mkdir -p "$DEST"

find "$SOURCE" -type f -name "*.mns" | while IFS= read -r file;do
    relative_path="${file#"$SOURCE"/}"
    output_file="$DEST/$relative_path"

    mkdir -p "$(dirname "$output_file")"

    sed \
        -e '/^\*-/d' \
        -e '/\*M/d' \
        -e '/^\.$/d' \
        -e '/^!/d' \
        -e '/^\*k\[\]/d' \
        -e 's/[ip]//g' \
        "$file" > "$output_file"

done
