# FROM nvidia/cuda:12.3.1-base-ubuntu22.04
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    cmake \
    python3 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# OPENMVG INSTALLATION
RUN apt-get update && apt-get install -y \
                libpng-dev \
                libjpeg-dev \
                libtiff-dev \
                libxxf86vm1 \
                libxxf86vm-dev \
                libxi-dev \
                libxrandr-dev \
                graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --recursive https://github.com/openMVG/openMVG.git

RUN mkdir openMVG_Build && cd openMVG_Build \
    && cmake -DCMAKE_BUILD_TYPE=RELEASE ../openMVG/src/ \
    && cmake --build . --target install -j 10 && cd ..


# OPENMVS INSTALLATION
RUN apt-get update && apt-get install -y \
                libpng-dev \
                libjpeg-dev \
                libtiff-dev \
                libglu1-mesa-dev \
                libboost-iostreams-dev \
                libboost-program-options-dev \
                libboost-system-dev \
                libboost-serialization-dev \
                libopencv-dev \
                libcgal-dev \
                libcgal-qt5-dev \
                libatlas-base-dev \
                libsuitesparse-dev \
                freeglut3-dev \
                libglew-dev \
                libglfw3-dev \
    && rm -rf /var/lib/apt/lists/*

# Eigen installation
RUN git clone https://gitlab.com/libeigen/eigen.git --branch 3.4 \
    && mkdir eigen_build && cd eigen_build \
    && cmake ../eigen \
    && make && make install -j10 \
    && cd .. && rm -rf eigen_build eigen

# VCGLib installation
RUN git clone https://github.com/cdcseacave/VCG.git vcglib

# Ceres Solver installation (Optional)
RUN git clone https://ceres-solver.googlesource.com/ceres-solver ceres-solver \
    && mkdir ceres_build && cd ceres_build \
    && cmake ../ceres-solver/ -DMINIGLOG=ON -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF \
    && make -j10 && make install \
    && cd .. && rm -rf ceres_build ceres-solver


RUN git clone https://github.com/cdcseacave/openMVS.git openMVS
RUN mkdir openMVS_build
WORKDIR /app/openMVS_build
# RUN cmake ../openMVS -DCMAKE_BUILD_TYPE=Release -DVCG_ROOT="../vcglib"
RUN cmake ../openMVS -DCMAKE_BUILD_TYPE=Release -DVCG_ROOT="../vcglib" -DCMAKE_INSTALL_PREFIX=/app/OpenMVS
RUN make install -j10
WORKDIR /app
RUN rm -rf openMVS_build openMVS



# RUN PIPELINE 
COPY . /app
RUN pip3 install --upgrade pip

# INSTALL PYTHON DEPENDENCIES
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt


# # RUN PYTHON SCRIPT
# CMD ["python3", "main.py"]




