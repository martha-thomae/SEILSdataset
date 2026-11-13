cd SEILSdataset/SEILS_diplomatic_OMRgroundTruth/particellas_codified
mkdir -p ../extracted_spines

for file in *.mns; do
    extract -i '**mens' "$file" > "../extracted_spines/$file"
done