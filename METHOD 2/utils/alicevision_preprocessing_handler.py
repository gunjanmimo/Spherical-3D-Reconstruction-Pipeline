import os
import subprocess
from glob import glob

aliceVision_image_spliter_executable_path = (
    "/Meshroom-2023.3.0/aliceVision/bin/aliceVision_split360Images"
)


def aliceVision_preprocessing_handler(
    img_dir: str,
    output_dir: str,
    number_of_splits: int,
) -> bool:

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # check if the executable exists
    if not os.path.exists(aliceVision_image_spliter_executable_path):
        assert False, "ERROR: AliceVision executable not found"

    # run the executable
    subprocess.run(
        [
            aliceVision_image_spliter_executable_path,
            "-i",
            img_dir,
            "-o",
            output_dir,
            "--outSfMData",
            os.path.join(output_dir, "sfm"),
            "--equirectangularNbSplits",
            str(number_of_splits),
            "-v",
            "debug",
        ]
    )

    # arrange data

    splitted_img_dir = os.path.join(output_dir, "rig")
    print(f"INFO: Split images are saved in {splitted_img_dir}")

    all_splitted_img_paths = glob(os.path.join(splitted_img_dir, "**/*.j*"))
    assert len(all_splitted_img_paths) > 0, "No images found in the data directory"

    final_img_dir = os.path.join(output_dir, "final_images")
    os.makedirs(final_img_dir, exist_ok=True)

    for i, image in enumerate(all_splitted_img_paths):
        os.system(f"cp {image} {final_img_dir}/{i}.jpg")

    print("INFO: AliceVision preprocessing completed")

    return True
