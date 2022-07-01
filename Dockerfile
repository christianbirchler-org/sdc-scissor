FROM python:3.9.6-slim

RUN apt-get update \
  && apt-get install -y \
    gcc \
    python3-opengl \
  && rm -rf /var/lib/apt/lists/*

ENV SHELL=/bin/bash
ARG POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /var/project

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . ./

ENTRYPOINT ["poetry", "run", "sdc-scissor"]
