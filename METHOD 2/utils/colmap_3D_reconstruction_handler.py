import os
import subprocess


def colmap_3D_reconstruction_handler(image_dir: str, output_dir: str) -> bool:

    print(f"\n\n\nimage_dir-------------------------------> {image_dir}\n\n\n")

    colmap_dir = os.path.join(output_dir, "COLMAP")
    os.makedirs(colmap_dir, exist_ok=True)

    database_path = os.path.join(colmap_dir, "database.db")
    spare_dir = os.path.join(colmap_dir, "sparse")
    dense_dir = os.path.join(colmap_dir, "dense")
    ply_path = os.path.join(colmap_dir, "pointcloud.ply")

    print("Running COLMAP reconstruction...")

    # Feature extraction
    print("Feature extraction")
    print("~" * 50)
    command_feature_extraction = f"""

        colmap feature_extractor --ImageReader.single_camera=1 \
            --ImageReader.camera_model=SIMPLE_PINHOLE \
            --database_path {database_path} \
            --image_path {image_dir}\
            --SiftExtraction.use_gpu=1
            """
    print(command_feature_extraction)
    os.system(command=command_feature_extraction)

    # Image matching
    print("Image matching")
    print("~" * 50)
    command_exhaustive_matcher = f"""
        colmap exhaustive_matcher \
            --database_path {database_path} \
            --SiftMatching.use_gpu=1
    """
    os.system(command=command_exhaustive_matcher)

    # Sparse reconstruction
    print("Sparse reconstruction")
    print("~" * 50)
    command_3D_reconstruction = f"""
        mkdir {spare_dir}

        colmap mapper \
            --database_path {database_path} \
            --image_path {image_dir} \
            --output_path {spare_dir}

    """
    os.system(command=command_3D_reconstruction)

    # Model conversion
    print("Model conversion")
    print("~" * 50)
    command_model_converter = f"""
        colmap model_converter \
            --input_path {spare_dir}/0 \
            --output_path {ply_path} \
            --output_type PLY

    """
    os.system(command=command_model_converter)
    # DENSE RECONSTRUCTION
    command_dense_reconstruction = f"""
        mkdir {dense_dir}
        
        colmap image_undistorter \
            --image_path {image_dir} \
            --input_path {spare_dir}/0 \
            --output_path {dense_dir} \
            --output_type COLMAP \
            --max_image_size 4000
            
        colmap patch_match_stereo \
            --workspace_path {dense_dir} \
            --workspace_format COLMAP \
            --PatchMatchStereo.geom_consistency true
        
        colmap stereo_fusion \
            --workspace_path {dense_dir} \
            --workspace_format COLMAP \
            --input_type geometric \
            --output_path {dense_dir}/fused.ply
        
        colmap poisson_mesher \
            --input_path {dense_dir}/fused.ply \
            --output_path {dense_dir}/meshed-poisson.ply
        
        colmap delaunay_mesher \
            --input_path {dense_dir}/fused.ply \
            --output_path {dense_dir}/meshed-delaunay.ply
            
    
    
    """

    os.system(command=command_dense_reconstruction)
    return True
