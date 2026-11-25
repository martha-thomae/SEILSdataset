import re
from pathlib import Path


CLEF_DEFAULT = "*clefG2"

input_dir = Path("cleaned_mens_spines")
output_dir = Path("staff_segmented_mens")

output_dir.mkdir(exist_ok=True)


f = 0
clef = CLEF_DEFAULT

for file_path in input_dir.iterdir():
    if file_path.is_file() and file_path.suffix == ".mns":
        f += 1
        print(f"{f}: Processing {file_path}")

        piece_content = file_path.read_text(encoding="utf-8")

        staff_partitions = piece_content.split("=-")

        for i, staff_content in enumerate(staff_partitions):
            # Split the staff content into tokens to:
            stafftokens = staff_content.splitlines()
            # (1) retrieve the clef (and key signature) from the first staff
            if i == 0:
                clef_matches = [token for token in stafftokens if re.search(r"\*clef..", token)]
                staff0_last_clef = clef_matches[-1]
                keysig_matches = [token for token in stafftokens if re.search(r"\*k\[.*\]", token)]
            # (2) add that clef (and key signature) as the first token for all other staves of the same piece/work
            else:
                stafftokens.pop(0) # Remove the first token, which is an empty one for all staves other than the first
                stafftokens.insert(0, "**mens")
                stafftokens.insert(1, staff0_last_clef)
                # Only if there was a key signature in the voice (as empty key signature tokens '*k[]' have been removed)
                if len(keysig_matches) != 0: 
                    staff0_last_keysig = keysig_matches[-1]
                    stafftokens.insert(2, staff0_last_keysig)

            staff_content = "\n".join(stafftokens)
            staff_content = staff_content + "\n"
            output_path = output_dir / f"{file_path.stem}_staff{i+1}.mns"
            output_path.write_text(staff_content, encoding="utf-8")

# Especial files that have an extra clef on line # 4 (list item # 3)
files = [
    "marenzio_mentrelaura_A_staff4.mns",
    "marenzio_mentrelaura_B_staff4.mns",
    "marenzio_mentrelaura_C_staff4.mns",
    "marenzio_mentrelaura_Q_staff4.mns",
    "marenzio_mentrelaura_T_staff4.mns"
]
for file in files:
    with (output_dir/file).open("r", encoding="utf-8") as ifile:
        lines = ifile.readlines()
    # Remove line # 4 (item # 3), the duplicated clef
    newlines = lines[0:3]+lines[4:]
    with (output_dir/file).open("w", encoding="utf-8") as ofile:
        ofile.writelines(newlines)
