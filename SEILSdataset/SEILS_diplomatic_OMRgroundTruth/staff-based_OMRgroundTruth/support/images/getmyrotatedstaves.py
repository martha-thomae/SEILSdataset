import json
import math
from pathlib import Path
from PIL import Image


OUTPUT_DIR = Path("staff-regions")


def extract_rotated_region(image, x, y, width, height, angle):
    """
    Extract a rotated rectangular region from an image.

    x, y, width, height: Label Studio coordinates (percentages).
    angle: rotation in degrees.
    """

    # Convert percentages to image pixels
    x *= image.width / 100
    y *= image.height / 100
    width *= image.width / 100
    height *= image.height / 100

    # Calculate the center of the bounding box
    cx = x + width / 2
    cy = y + height / 2

    # Label Studio positive angles are clockwise in image coordinates.
    theta = math.radians(angle)

    # Calculate the four rotated corners
    corners = []

    for dx, dy in [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2)
    ]:
        rx = dx * math.cos(theta) - dy * math.sin(theta) + cx
        ry = dx * math.sin(theta) + dy * math.cos(theta) + cy

        corners.append((rx, ry))

    # Get the enclosing axis-aligned rectangle
    min_x = math.floor(min(p[0] for p in corners))
    min_y = math.floor(min(p[1] for p in corners))
    max_x = math.ceil(max(p[0] for p in corners))
    max_y = math.ceil(max(p[1] for p in corners))

    # Crop the entire enclosing rectangle from the original image
    cropped = image.crop((min_x, min_y, max_x, max_y))

    # Rotate the crop to compensate for the original rotation
    if angle != 0:
        cropped = cropped.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=True,
            fillcolor="white"
        )

    # Extract the original bounding-box dimensions from the center
    final_width = round(width)
    final_height = round(height)

    center_x = cropped.width / 2
    center_y = cropped.height / 2

    cropped = cropped.crop((
        round(center_x - final_width / 2),
        round(center_y - final_height / 2),
        round(center_x + final_width / 2),
        round(center_y + final_height / 2)
    ))

    return cropped


def main():
    print("-- START --")

    filepath = Path("staff-regions.json")

    with filepath.open("r", encoding="utf-8") as f:
        images_in_corpus = json.load(f)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for img in images_in_corpus:
        pieceNameVoiceNo = img["image"]
        print(f"PROCESSING: {pieceNameVoiceNo}")

        staves = sorted(img["label"], key=lambda staff: staff["y"])

        with Image.open(pieceNameVoiceNo) as image:

            for i, staff in enumerate(staves):

                cropped = extract_rotated_region(
                    image,
                    x=staff["x"],
                    y=staff["y"],
                    width=staff["width"],
                    height=staff["height"],
                    angle=staff["rotation"]
                )

                output_file = (
                    OUTPUT_DIR /
                    f"{Path(pieceNameVoiceNo).stem}_staff{i+1}.png"
                )

                cropped.save(output_file)

                print(f"- Saved staff region {i+1}: {output_file}")

        print("Completed\n")

    print("-- END --")


if __name__ == "__main__":
    main()