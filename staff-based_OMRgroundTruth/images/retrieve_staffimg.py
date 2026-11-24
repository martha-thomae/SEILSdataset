import json
import math
from pathlib import Path
from PIL import Image


OUTPUT_DIR = Path("staff-regions")


def extract_rotated_region(image, x, y, width, height, angle):
    """
    Extract a rotated rectangular region from an image.

    x, y, width, height: Label Studio coordinates (percentages).
    angle: rotation in degrees, clockwise in image coordinates.

    Rotation origin: top-left corner (x, y).
    """

    # Convert percentages to image pixels
    x *= image.width / 100
    y *= image.height / 100
    width *= image.width / 100
    height *= image.height / 100

    theta = math.radians(angle)

    cos_a = math.cos(theta)
    sin_a = math.sin(theta)

    # Rotate corners around the top-left corner
    corners = [
        (x, y),
        (x + width * cos_a, y + width * sin_a),
        (x + width * cos_a - height * sin_a,
         y + width * sin_a + height * cos_a),
        (x - height * sin_a, y + height * cos_a)
    ]

    # Calculate enclosing axis-aligned rectangle
    min_x = math.floor(min(p[0] for p in corners))
    min_y = math.floor(min(p[1] for p in corners))
    max_x = math.ceil(max(p[0] for p in corners))
    max_y = math.ceil(max(p[1] for p in corners))

    # Crop enclosing rectangle
    cropped = image.crop((min_x, min_y, max_x, max_y))

    # Transform coordinates to the cropped image
    local_corners = [
        (px - min_x, py - min_y)
        for px, py in corners
    ]

    # Extract the rotated rectangle using a perspective transform.
    # Map the rotated quadrilateral to a horizontal rectangle.
    output_width = round(width)
    output_height = round(height)

    src = [
        local_corners[0],
        local_corners[1],
        local_corners[2],
        local_corners[3]
    ]

    # Pillow QUAD transform expects the source quadrilateral
    # in TL, BL, BR, TR order.
    quad = [
        src[0],
        src[3],
        src[2],
        src[1]
    ]

    result = cropped.transform(
        (output_width, output_height),
        Image.Transform.QUAD,
        (
            quad[0][0], quad[0][1],
            quad[1][0], quad[1][1],
            quad[2][0], quad[2][1],
            quad[3][0], quad[3][1]
        ),
        resample=Image.Resampling.BICUBIC
    )

    return result


def main():
    print("-- START --")

    filepath = Path("staff-regions.json")

    with filepath.open("r", encoding="utf-8") as f:
        images_in_corpus = json.load(f)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for img in images_in_corpus:
        pieceNameVoiceNo = img["image"]
        print(f"PROCESSING: {pieceNameVoiceNo}")

        # Retrieve staves corresponding to that image (using img['label'])
        # and order them according to their 'y' coordinate. So that staff
        # region 1 is the first staff on the page, and all others follow.
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
