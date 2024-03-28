import os
from glob import glob
import cv2
from tqdm import tqdm
import warnings

valid_image_extensions = [
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
    ".bmp",
    ".ppm",
    ".pgm",
    ".webp",
]


def image_format_handler(image_dir: str, extension: str, output_dir: str):

    # check if the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # all image path
    image_paths = glob(os.path.join(image_dir, "*"))
    assert len(image_paths) > 0, "No image found in the directory"

    print(f"\nTotal images found: {len(image_paths)}")

    extension_count_tracker = {}
    for image_path in tqdm(image_paths, desc="Validating image format "):
        file_extension = os.path.splitext(image_path)[-1].lower()
        if file_extension in valid_image_extensions:
            if file_extension in extension_count_tracker:
                extension_count_tracker[file_extension] += 1
            else:
                extension_count_tracker[file_extension] = 1

            # read image
            image = cv2.imread(image_path)
            # save image with new extension
            new_image_path = image_path.replace(file_extension, f".{extension}").split(
                "/"
            )[-1]
            new_image_path = os.path.join(output_dir, new_image_path)
            cv2.imwrite(new_image_path, image)

        else:
            warnings.warn(
                f"SKIPPING: Invalid image format: {image_path.split(" / ")[-1]}"
            )

    print("\nImage format conversion summary")
    print("#################################")
    for extension, count in extension_count_tracker.items():
        print(f"{extension}: {count} images")

    print("\nImage format conversion completed")
    return True
