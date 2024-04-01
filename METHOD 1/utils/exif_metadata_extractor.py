import os
import json
from glob import glob
from tqdm import tqdm

from PIL import Image
from PIL.ExifTags import TAGS
import warnings

"""
IMPORTANT METADATA TAGS


ImageWidth: 
ImageLength: 
Make
Model
DateTime
ApertureValue
BrightnessValue
ExposureBiasValue
MaxApertureValue
SubjectDistance
FocalLength

"""

desired_tags = [
    "ImageWidth",
    "ImageLength",
    "Make",
    "Model",
    "DateTime",
    "ApertureValue",
    "BrightnessValue",
    "ExposureBiasValue",
    "MaxApertureValue",
    "SubjectDistance",
    "FocalLength",
]


def read_image_exif(image_path):
    try:
        # Open the image
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                # List of EXIF tags we want to extract

                # Dictionary to store selected EXIF info
                exif_info = {}

                # Loop through all EXIF data items
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    # Check if the tag is one of the ones we want
                    if tag_name in desired_tags:
                        exif_info[tag_name] = (
                            float(value) if not isinstance(value, str) else value
                        )

                return exif_info
            else:
                # warnings.warn(f"{image_path.split('/')[-1]}: Found no EXIF data.")
                return {}
    except Exception as e:
        # warnings.warn(f"{image_path.split('/')[-1]}: Found no EXIF data.")
        return {}


def image_metadata_extractor(image_dir: str, output_dir: str):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_paths = glob(os.path.join(image_dir, "*"))
    assert len(image_paths) > 0, "No image found in the directory"

    meta_data = {}

    for file_path in tqdm(image_paths, desc="Extracting metadata"):
        file_name = file_path.split("/")[-1]
        meta_data[file_name] = read_image_exif(file_path)

    # save metadata to a file
    metadata_file = os.path.join(output_dir, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(meta_data, f, indent=4)

    print(f"\nMetadata extraction completed. Metadata saved to {metadata_file}")
    return True
