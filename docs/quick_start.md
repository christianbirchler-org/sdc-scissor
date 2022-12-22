# Quick Start
## Requirements
* Windows 10
* BeamNG.tech v0.24.0.2
* Python 3.9

````{note}
SDC-Scissor work currently only with BeamNG.tech v0.24.0.2!
````

You can install SDC-Scissor from PyPI or manually by downloading it from GitHub and install it with Poetry.
## PyPI
````shell
pip install sdc-scissor
sdc-scissor -c your_config.yml
````

## Manual installation
Clone the repository:
````shell
git clone https://github.com/ChristianBirchler/sdc-scissor.git
````

Install the dependencies:
````shell
cd sdc-scissor
poetry install
````

## Install BeamNG.tech
For using SDC-Scissor with the BeamNG.tech simulator you can obtain an academic license from BeamNG from their
[website](https://register.beamng.tech/). After installing BeamNG.tech you need to replace the `tig` level it in the
user directory of BeamNG.tech (`C:\Users\myaccount\Documents\BeamNG.drive\0.24\levels`) wth the one from this repository
(`levels_template/tig`).


## Run the tool
````shell
poetry run sdc-scissor -c sample_configs/label-tests.yml
````

The [Software Guidebook](software_guidebook/index.rst) provides more explanations about the
[installation](software_guidebook/deployment.md) and [usage](software_guidebook/operation_and_support.md) of
SDC-Scissor.

## Demo
[![](https://img.youtube.com/vi/Cn8p648KnfQ/maxresdefault.jpg)](https://youtu.be/Cn8p648KnfQ)

[YouTube Link](https://youtu.be/Cn8p648KnfQ)

## Data
In the repository is a directory `sample_tests` with some simple sample test cases. These tests are mainly used for
development purposes.

The data used for the demo and evaluation of SDC-Scissor v1.0 we made available on Zenodo:
[![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.5903161.svg)](https://doi.org/10.5281/zenodo.5903161)
````{note}
The used simulator was BeamNG.research which is deprecated and not compatible anymore with SDC-Scissor.
````
