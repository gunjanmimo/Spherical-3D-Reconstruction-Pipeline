# BACKEND ENGINEER ASSIGNMENT | FLOORFY 





### PROPOSED METHOD OVERVIEW

1. **METHOD 1**

**Method 1** used OpenMVG to do camera pose calculation and then it uses OpenMVS for Densify the generated pointcloud.

2. **METHOD 2**

**Method 2** uses AliceVision to preprocesse 360 images and then it uses Colmap sfm tool to generate sparse and dense pointcloud file.


### SETUP 

#### 1. DATA PREPARATION 


**FOLDER STRUCTURE**

```
.
└── data/
    ├── config.yaml
    └── images/
        ├── image_1.jpeg
        ├── image_2.jpeg
        └── image_N.jpeg
```

`config.yaml` contains different configuration to run the proposed methods. For details check **README.md** of individual method. 



**RUN PIPELINE**

Individual method folder has `Dockerfile` to run the 3D reconstruction pipeline.

To build the Docker image, run 

```
cd <method dir>
docker build -t pipeline .
```

To run the 3D pipeline and generate `.ply` file, use the following command 

```
docker run --gpus all -v <data folder path>:/app/data -t pipeline

```

It will save the final dense pointcloud `.ply` file. 