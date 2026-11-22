import json
from pathlib import Path
from PIL import Image


OUTPUT_DIR = Path("staff-regions")
ORIG_WIDTH = 1200
ORIG_HEIGHT = 813


def main():
    print("-- START --")
    filepath = Path("staff-regions.json")
    with filepath.open("r", encoding="utf-8") as f:
        images_in_corpus = json.load(f)
    
    for img in images_in_corpus:
        pieceNameVoiceNo = img["image"]
        print(f"PROCESSING: {pieceNameVoiceNo}")

        image = Image.open(pieceNameVoiceNo)

        staves = img["label"]
        staves = sorted(staves, key=lambda staff: staff["y"])
        for i, staff in enumerate(staves):
            x0 = staff["x"]
            y0 = staff["y"]
            x1 = x0 + staff["width"]
            y1 = y0 + staff["height"]
            coordinates = (
                x0/100*ORIG_WIDTH, 
                y0/100*ORIG_HEIGHT, 
                x1/100*ORIG_WIDTH, 
                y1/100*ORIG_HEIGHT
            )
            print(f"- Staff region {i+1}: {coordinates}")

            cropped = image.crop(coordinates)

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            output_file = OUTPUT_DIR / f"{Path(pieceNameVoiceNo).stem}_staff{i+1}.png"
            cropped.save(output_file)

        image.close()
        print("Completed\n")

    print("-- END --")


if __name__ == "__main__":
    main()

#still need to consider rotation
