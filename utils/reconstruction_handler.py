import os
import subprocess


def image_3D_reconstruction_handler(
    data_dir: str, camera_file_params_path: str
) -> bool:

    input_dir = os.path.join(data_dir, "images")
    output_dir = os.path.join(data_dir, "reconstruction")
    os.makedirs(data_dir, exist_ok=True)

    matches_dir = os.path.join(data_dir, "matches")
    os.makedirs(matches_dir, exist_ok=True)

    print("1. Intrinsics analysis")
    pIntrinsics = subprocess.Popen(
        [
            "openMVG_main_SfMInit_ImageListing",
            "-i",
            input_dir,
            "-o",
            matches_dir,
            "-d",
            camera_file_params_path,
            "-c",
            "7",
            "-f",
            "1",
            "-g",
            "1",
        ]
    )
    pIntrinsics.wait()

    print("2. Compute features")
    pFeatures = subprocess.Popen(
        [
            "openMVG_main_ComputeFeatures",
            "-i",
            matches_dir + "/sfm_data.json",
            "-o",
            matches_dir,
            "-m",
            "SIFT",
            "-f",
            "1",
            "-p",
            "ULTRA",
            "-n",
            "10",
        ]
    )
    pFeatures.wait()

    print("3. Compute matches")
    pMatches = subprocess.Popen(
        [
            "openMVG_main_ComputeMatches",
            "-i",
            matches_dir + "/sfm_data.json",
            "-o",
            matches_dir + "/matches.putative.bin",
            "-f",
            "1",
            "-n",
            "ANNL2",
        ]
    )
    pMatches.wait()

    print("4. Filter matches")
    pFiltering = subprocess.Popen(
        [
            "openMVG_main_GeometricFilter",
            "-i",
            matches_dir + "/sfm_data.json",
            "-m",
            matches_dir + "/matches.putative.bin",
            "-g",
            "f",
            "-o",
            matches_dir + "/matches.f.bin",
        ]
    )
    pFiltering.wait()

    reconstruction_dir = os.path.join(output_dir, "reconstruction_sequential")
    print(
        "5. Do Incremental/Sequential reconstruction"
    )  # set manually the initial pair to avoid the prompt question
    pRecons = subprocess.Popen(
        [
            "openMVG_main_SfM",
            "--sfm_engine",
            "INCREMENTALV2",
            "--input_file",
            matches_dir + "/sfm_data.json",
            "--match_dir",
            matches_dir,
            "--output_dir",
            reconstruction_dir,
        ]
    )
    pRecons.wait()

    print("6. Colorize Structure")
    pRecons = subprocess.Popen(
        [
            "openMVG_main_ComputeSfM_DataColor",
            "-i",
            reconstruction_dir + "/sfm_data.bin",
            "-o",
            os.path.join(reconstruction_dir, "colorized.ply"),
        ]
    )
    pRecons.wait()

    print("7. Structure from Known Poses (robust triangulation)")
    pRecons = subprocess.Popen(
        [
            "openMVG_main_ComputeStructureFromKnownPoses",
            "-i",
            reconstruction_dir + "/sfm_data.bin",
            "-m",
            matches_dir,
            "-o",
            os.path.join(reconstruction_dir, "robust.ply"),
        ]
    )
    pRecons.wait()

    print(f"Reconstruction completed. Output saved in {reconstruction_dir}")

    return True
