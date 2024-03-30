FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# INSTALL COLMAP DEPENDENCIES
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    cmake \
    ninja-build \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev

# BUILD COLMAP
RUN git clone https://github.com/colmap/colmap.git
WORKDIR /colmap

RUN mkdir build && \
    cd build && \
    cmake .. -GNinja && \
    ninja && ninja install


# INSTALL ALICEVISION
WORKDIR /
RUN wget https://github.com/alicevision/Meshroom/releases/download/v2023.3.0/Meshroom-2023.3.0-linux.tar.gz && \
    tar -xzf Meshroom-2023.3.0-linux.tar.gz && \
    rm Meshroom-2023.3.0-linux.tar.gz && \
    ls /Meshroom-2023.3.0/aliceVision/lib/libaliceVision_cmdline.so.3.2

ENV ALICEVISION_ROOT=/Meshroom-2023.3.0/aliceVision
ENV LD_LIBRARY_PATH=/Meshroom-2023.3.0/aliceVision/lib:$LD_LIBRARY_PATH

