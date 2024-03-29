FROM ubuntu:22.04

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

COPY . /app
RUN pip3 install --upgrade pip

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

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




# RUN PYTHON SCRIPT
CMD ["python3", "main.py"]


