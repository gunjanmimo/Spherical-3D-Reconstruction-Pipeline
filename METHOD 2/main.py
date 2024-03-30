import os
from glob import glob
import yaml
import subprocess

# local imports
from utils import (
    image_format_handler,
    image_resolution_handler,
    image_orientation_handler,
    image_metadata_extractor,
    aliceVision_preprocessing_handler,
    colmap_3D_reconstruction_handler,
)


def main(
    img_dir: str,
    output_dir: str,
    extension: str,
    max_width: int,
    max_height: int,
    orientation: str,
    aliceVision_number_of_splits: int,
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
    print("\nSTAGE 5: AliceVision 360 DEGREE IMAGE PREPROCESSING")
    print("=====================================")
    aliceVision_preprocessing_handler(
        img_dir=os.path.join(output_dir, "images"),
        output_dir=os.path.join(output_dir, "output_split"),
        number_of_splits=aliceVision_number_of_splits,
    )

    # stage 6: 3D reconstruction using COLMAP
    print("\nSTAGE 6: COLMAP 3D RECONSTRUCTION")
    print("=====================================")
    colmap_3D_reconstruction_handler(
        image_dir=os.path.join(output_dir, "output_split", "final_images"),
        output_dir=output_dir,
    )

    return


if __name__ == "__main__":

    print("\n-----------------------------------")
    print("Image Processing & 3D Reconstruction Pipeline")
    print("-----------------------------------")

    root_dir = "data"
    # load yaml file
    with open(os.path.join(root_dir, "config.yaml"), "r") as file:
        config = yaml.safe_load(file)

    img_dir = os.path.join(root_dir, "images")
    output_dir = os.path.join(root_dir, "output")
    extension = config.get("extension", "jpeg")
    max_width = config.get("max_width", None)
    max_height = config.get("max_height", None)
    orientation = config.get("orientation", "landscape")
    aliceVision_number_of_splits = config.get("aliceVision_number_of_splits", 8)

    main(
        img_dir=img_dir,
        output_dir=output_dir,
        extension=extension,
        max_width=max_width,
        max_height=max_height,
        orientation=orientation,
        aliceVision_number_of_splits=aliceVision_number_of_splits,
    )
