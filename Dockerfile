FROM python:3.9.6-slim

RUN apt-get update \
  && apt-get install -y \
    gcc \
    # Update insecure packages
    libsystemd0=241-7~deb10u8 \
    libudev1=241-7~deb10u8 \
  && rm -rf /var/lib/apt/lists/*

ENV SHELL=/bin/bash
ARG POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /var/project

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . ./

ENTRYPOINT ["poetry", "run", "python", "sdc-scissor.py"]
