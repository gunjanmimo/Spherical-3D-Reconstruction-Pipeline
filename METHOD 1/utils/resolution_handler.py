import os
from glob import glob
from PIL import Image
from tqdm import tqdm


def image_resolution_handler(
    image_dir: str, max_width: int = None, max_height: int = None
) -> bool:
    image_paths = glob(os.path.join(image_dir, "*"))

    all_widths = []
    all_heights = []

    for image_path in tqdm(image_paths, desc="Checking image resolution "):
        image = Image.open(image_path)
        width, height = image.size
        all_widths.append(width)
        all_heights.append(height)

    avg_width = sum(all_widths) / len(all_widths)
    avg_height = sum(all_heights) / len(all_heights)

    avg_width = int(avg_width)
    avg_height = int(avg_height)

    if max_width and max_height:
        # Resize images to max_width and max_height
        for image_path in tqdm(image_paths, desc="Resizing images "):
            image = Image.open(image_path)
            image = image.resize((max_width, max_height))
            image.save(image_path)
    else:
        # Resize images to average width and height
        for image_path in tqdm(image_paths, desc="Resizing images "):
            image = Image.open(image_path)
            if image.size != (avg_width, avg_height):
                image = image.resize(avg_width, avg_height)
                image.save(image_path)

    print(f"Images resized to {avg_width}x{avg_height} pixels.")
    print("Resolution check complete.")
    return True
