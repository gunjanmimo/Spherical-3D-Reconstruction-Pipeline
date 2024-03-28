import os
from glob import glob
from PIL import Image
from tqdm import tqdm


def image_orientation_handler(image_dir: str, orientation: str = None) -> bool:

    image_paths = glob(os.path.join(image_dir, "*"))

    """
    Check image orientation and rotate if necessary
    note: 360-degree panoramas (width is 2 times height)
    """

    wrong_orientation_count = 0
    for image_path in tqdm(image_paths, desc="Checking image orientation "):
        image = Image.open(image_path)
        width, height = image.size
        if width > height:
            if orientation == "landscape":
                pass
            else:
                image = image.rotate(90, expand=True)
                image.save(image_path)
                wrong_orientation_count += 1
        elif height > width:
            if orientation == "portrait":
                pass
            else:
                image = image.rotate(90, expand=True)
                image.save(image_path)
                wrong_orientation_count += 1
        else:
            pass

    print(f"Images with wrong orientation: {wrong_orientation_count}")
    print("Orientation check complete.")
    return True
