FROM python:3.9-bookworm

SHELL ["/bin/bash", "-c"]

# https://pythonspeed.com/articles/activate-conda-dockerfile/
ENV PROJECT_ROOT=/root \
    PROJECT_NAME=GoldenSource

ENV ENV=UAT \
    PROJECT_SRC_DIR=${PROJECT_ROOT}/src/${PROJECT_NAME} \
    PROJECT_BUILD_DIR=${PROJECT_ROOT}/build/${PROJECT_NAME} \
    PYTHON_VENV_DIR=${PROJECT_ROOT}/build/venv/${PROJECT_NAME} \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache 

WORKDIR ${PROJECT_BUILD_DIR}

COPY cfg/${ENV}/. cfg/.

WORKDIR ${PYTHON_VENV_DIR}

RUN apt-get update \
    && apt-get -y install gcc g++ vim unixodbc \
    && rm -rf /var/lib/apt/lists/* 

RUN python -m venv .

WORKDIR ${PROJECT_SRC_DIR}    

COPY pyproject.toml poetry.lock README.md ./
COPY GoldenSource ./GoldenSource
COPY iceobject ./iceobject

RUN source ${PYTHON_VENV_DIR}/bin/activate \
    && pip install --upgrade pip \ 
    && pip install poetry==1.8.1 toml \
    && poetry install && rm -rf $POETRY_CACHE_DIR

ENV VIRTUAL_ENV=${PYTHON_VENV_DIR} \
    PATH=${PYTHON_VENV_DIR}/bin:${PATH} \
    ICEOBJECT_SRC=${PROJECT_SRC_DIR}/iceobject/platform \
    ICEOBJECT_BUILD=${PROJECT_BUILD_DIR}/iceobject
    
ENV PYTHONPATH=${ICEOBJECT_BUILD}:${PROJECT_SRC_DIR}:${PYTHONPATH}

RUN python iceobject/python/slice2py.py --source_dir ${ICEOBJECT_SRC} --destination_dir ${ICEOBJECT_BUILD}
RUN python -m unittest discover -s . -p "*_test.py" -v