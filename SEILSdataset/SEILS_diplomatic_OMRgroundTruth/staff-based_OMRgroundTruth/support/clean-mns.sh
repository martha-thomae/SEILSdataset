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
        -e '/^\*$/d' \
        -e '/^!/d' \
        -e '/^\*k\[\]/d' \
        -e '/^\*staff./d' \
        -e 's/[ip]//g' \
        "$file" > "$output_file"

done

# Now, I want to merge the mensuration sign info of `*met(C)\n*met(3/2)` into the one mensuration sign `*met(C3/2)` for the five voices in virchi_arsimentre (A,B,C,Q: staff 5 & T: staff 6)

# We can always clean up the 'extracted spines' first, before dividing them into staves.
# Current workflow: extract_mens_spines.sh , divide_into_staves.py , clean-mns.sh , tokenizer.py
# We can change it for: extract_mens_spines.sh , clean-mns.sh , divide_into_staves.py , tokenizer.py
