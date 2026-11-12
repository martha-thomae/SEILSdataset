import re
from pathlib import Path


CLEF_DEFAULT = "*clefG2"

input_dir = Path("extracted_spines")
output_dir = Path("partitioned")

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
            # (1) retrieve the clef from the first staff
            if i == 0:
                matches = [token for token in stafftokens if re.search(r"\*clef..", token)]
                staff0_last_clef = matches[-1]
            # (2) add that clef as the first token for all other staves of the same piece/work
            else:
                stafftokens.pop(0) # Remove the first token, which is an empty one for all staves other than the first
                stafftokens.insert(0, "**mens")
                stafftokens.insert(1, staff0_last_clef)

            staff_content = "\n".join(stafftokens)
            output_path = output_dir / f"{file_path.stem}_staff{i+1}.mns"
            output_path.write_text(staff_content, encoding="utf-8")
