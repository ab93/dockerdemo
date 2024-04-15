# Base
FROM python:3.12-bookworm as initial

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# copy src files
COPY ./src /app/src

# copy requirements and extension dir
COPY ./requirements.txt ./extension /app/

# install python dependencies
RUN pip install -r requirements.txt

# install non-python dependencies
RUN python setup.py install

EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]


# Better order
FROM python:3.12-bookworm as better_order

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# copy requirements and extension dir
COPY ./requirements.txt ./extension /app/

# install python dependencies
RUN pip install -r requirements.txt

# install non-python dependencies
RUN python setup.py install

# copy src files
COPY ./src /app/src

EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]


# 1. Pin Transitive Dependencies
# 2. Disable pip cache
FROM python:3.12-bookworm as poetryexport

# disable pip cache
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY ./requirements-exported.txt ./extension /app/

# install python dependencies
RUN pip install -r requirements-exported.txt

# install non-python dependencies
RUN python setup.py install

COPY ./src /app/src

EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]


# Use slim base image
FROM python:3.12-slim-bookworm as slimmed_err

# disable pip cache
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY ./requirements-exported.txt ./extension /app/

# install python dependencies
RUN pip install -r requirements-exported.txt

# install non-python dependencies
# this will FAIL!
RUN python setup.py install

COPY ./src /app/src

EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]


# 1. Use slim base image
# 2. Install C++ compiler
# 3. Remove compiler after build
FROM python:3.12-slim-bookworm as slimmed

# disable pip cache
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y g++

WORKDIR /app

# copy requirements and extension dir
COPY ./requirements-exported.txt ./extension /app/

RUN pip install -r requirements-exported.txt
RUN python setup.py install
RUN apt-get purge -y --auto-remove g++

COPY ./src /app/src

EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]



# Combine layers
FROM python:3.12-slim-bookworm as single_layer

# disable pip cache
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# copy requirements and extension dir
COPY ./requirements-exported.txt ./extension /app/

# build dependencies
RUN apt-get update \
    && apt-get install -y g++ \
    && pip install -r requirements-exported.txt \
    && python setup.py install \
    && apt-get purge -y --auto-remove g++

# copy src files
COPY ./src /app/src

EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]


FROM python:3.12-bookworm as builder

ENV VIRTUAL_ENV=/opt/venv \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements-exported.txt extension ./

RUN pip install setuptools \
    && pip install -r requirements-exported.txt \
    && python setup.py install

FROM python:3.12-slim-bookworm AS multistage_runner_1

ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY ./src /app/src


EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]


FROM python:3.12-bookworm as mntcache_builder

ENV VIRTUAL_ENV=/opt/venv \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements-exported.txt extension ./

RUN --mount=type=cache,target=/root/.cache/pip pip install setuptools \
    && pip install -r requirements-exported.txt \
    && python setup.py install


FROM python:3.12-slim-bookworm AS multistage_runner_2

ENV VIRTUAL_ENV=/opt/venv
COPY --from=mntcache_builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY ./src /app/src


EXPOSE 80
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "80"]