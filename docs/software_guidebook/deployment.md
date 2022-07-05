# Deployment
This section provides information about the mapping between the
[software architecture](https://sdc-scissor.readthedocs.io/en/latest/software_guidebook/software_architecture.html)
and the
[infrastructure architecture](https://sdc-scissor.readthedocs.io/en/latest/software_guidebook/infrastructure_architecture.html).

## Simulator
To use the full potential of SDC-Scissor you should follow the installation guidelines of the desired simulator provided
on the according website of the simulator's provider.

## Installing SDC-Scissor
The tool can either be run locally using [Poetry](https://python-poetry.org/docs/) (**RECOMMENDED**) or with
[Docker](https://docs.docker.com/get-docker/).

## Requirements
* BeamNG
    * When running the simulations a working installation of [BeamNG.tech version 0.24](https://beamng.tech) is required.
    * Additionally, this simulation cannot be run in a Docker container but must run locally.
* `Python 3.9`
    * Note: `SDC-Scissor` is tested with this version of python only
* [Poetry](https://python-poetry.org/docs/)
* [Docker](https://docs.docker.com/get-docker/)

## BeamNG
For using SDC-Scissor with the BeamNG.tech simulator you can obtain an academic license from BeamNG from their
[website](https://register.beamng.tech/). After installing BeamNG.tech you need to replace the `tig` level it in the
user directory of BeamNG.tech (`C:\Users\myaccount\Documents\BeamNG.drive\0.24\levels`) wth the one from this repository
(`levels_template/tig`).

## Installation commands
To install the ``SDC-Scissor``, use one of the following approaches:

* Docker: `docker build --tag sdc-scissor .`
* Poetry: `poetry install`
