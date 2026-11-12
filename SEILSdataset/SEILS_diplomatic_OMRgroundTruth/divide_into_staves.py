from pathlib import Path

input_dir = Path("extracted_spines")
output_dir = Path("partitioned")

output_dir.mkdir(exist_ok=True)

f = 0
for file_path in input_dir.iterdir():
    if file_path.is_file() and file_path.suffix == ".mns":
        f += 1
        print(f"{f}: Processing {file_path}")
        content = file_path.read_text(encoding="utf-8")

        staff_partitions = content.split("=-")

        for i, staff_content in enumerate(staff_partitions):
            output_path = output_dir / f"{file_path.stem}_staff{i+1}.mns"
            output_path.write_text(staff_content, encoding="utf-8")
