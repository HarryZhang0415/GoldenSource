# SETUP PYTHON IMAGE
FROM python:3.9-bookworm AS python

# SETUP DEBIAN IMAGE
FROM python as debian

RUN apt-get update

RUN apt-get -y install --no-install-recommends \
    gcc \
    g++ \
    make

RUN apt-get -y install --no-install-recommends \
    git

RUN apt-get -y install --no-install-recommends \
    curl \
    wget

RUN apt-get -y install --no-install-recommends \
    libsm6 \
    libxt6 \
    libgl1-mesa-glx \
    libpng16-16 \
    libwebkit2gtk-4.0-dev \
    build-essential \
    libssl-dev \
    librsvg2-dev \
    ffmpeg \
    python3-tk

RUN apt-get clean

# SETUP POETRY IMAGE
FROM debian as poetry

ENV ROOT=/root \
    PROJECT_NAME=DataMart

# Define the version of Poetry to install (default is 1.4.2)
# Define the directory of python virtual environment

ENV ENV=UAT \
    PROJECT_SRC_DIR=${ROOT}/src/GoldenSource/${PROJECT_NAME} \
    PROJECT_BUILD_DIR=${ROOT}/build/GoldenSource/${PROJECT_NAME} \
    PYTHON_VENV_DIR=${ROOT}/build/GoldenSource/venv/${PROJECT_NAME} \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=true \
    POETRY_CACHE_DIR=/tmp/poetry_cache 

ARG POETRY_VERSION=1.8.2    

# Create a Python virtual environment for Poetry and install it
RUN python3 -m venv ${PYTHON_VENV_DIR} && \
    $PYTHON_VENV_DIR/bin/pip install --upgrade pip wheel && \
    $PYTHON_VENV_DIR/bin/pip install poetry==${POETRY_VERSION} toml

ENV PATH="$PYTHON_VENV_DIR/bin:$PATH" \
    VIRTUAL_ENV=$PYTHON_VENV_DIR

ENV PYTHONPATH=${ICEOBJECT_BUILD}:${PROJECT_SRC_DIR}:${PYTHONPATH}

# SETUP DataMart IMAGE
FROM poetry as datamart-uat

WORKDIR ${PROJECT_BUILD_DIR}

COPY ./cfg/${ENV} ./cfg

RUN mkdir ${PROJECT_BUILD_DIR}/DataMartUserData

# Set the working directory for the app
WORKDIR ${PROJECT_SRC_DIR}

COPY ./DataMart ./

RUN python dev_install.py

