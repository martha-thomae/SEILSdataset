#!/bin/bash

mkdir -p ./extracted_mens_spines

input_dir="../../particellas_codified"
for file in "$input_dir"/*.mns; do
	filename=$(basename "$file")
    extract -i '**mens' "$file" > "extracted_mens_spines/$filename"
done
