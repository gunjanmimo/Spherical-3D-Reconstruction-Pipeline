import os
from glob import glob
import argparse


# local imports
from utils import (
    image_format_handler,
    image_resolution_handler,
    image_orientation_handler,
    image_metadata_extractor,
)


def main(
    img_dir: str,
    output_dir: str,
    extension: str,
    max_width: int,
    max_height: int,
    orientation: str,
):

    # stage 1: collect image meta data
    print("\nSTAGE 1: Collecting image metadata")
    print("=====================================")
    image_metadata_extractor(
        image_dir=img_dir,
        output_dir=output_dir,
    )

    # stage 2: check file extension
    print("\nSTAGE 2: Checking image file extension")
    print("=====================================")
    image_format_handler(
        image_dir=img_dir,
        extension=extension,
        output_dir=os.path.join(output_dir, "images"),
    )
    # stage 3: image orientation
    print("\nSTAGE 3: Checking image orientation")
    print("=====================================")
    image_orientation_handler(
        image_dir=os.path.join(output_dir, "images"),
        orientation=orientation,
    )
    # stage 4: check image resolution
    print("\nSTAGE 4: Checking image resolution")
    print("=====================================")
    image_resolution_handler(
        image_dir=os.path.join(output_dir, "images"),
        max_width=max_width,
        max_height=max_height,
    )

    # stage 5: 3D reconstruction
    return


if __name__ == "__main__":

    print("\n-----------------------------------")
    print("Image Processing & 3D Reconstruction Pipeline")
    print("-----------------------------------")

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Image path")
    parser.add_argument("--output", type=str, required=True, help="Output path")
    parser.add_argument("--extension", type=str, help="Image extension", default="jpeg")
    parser.add_argument(
        "--max_width", type=int, help="Max width, default=average width", default=6000
    )
    parser.add_argument(
        "--max_height",
        type=int,
        help="Max height, default=average height",
        default=6000,
    )
    parser.add_argument(
        "--orientation",
        type=str,
        help="Orientation",
        default="landscape",
    )

    args = parser.parse_args()

    main(
        img_dir=args.input,
        output_dir=args.output,
        extension=args.extension,
        max_width=args.max_width,
        max_height=args.max_height,
        orientation=args.orientation,
    )
