# Quick Start
## Requirements
* Windows 10
* BeamNG.tech v0.24.0.2
* Python 3.9

You can install SDC-Scissor from PyPI or manually by downloading it from GitHub and install it with Poetry.
## PyPI
````shell
pip install sdc-scissor
sdc-scissor -c your_config.yml
````

## Manual installation
1. Clone the repository
````shell
git clone https://github.com/ChristianBirchler/sdc-scissor.git
````
2. Install dependencies
````shell
cd sdc-scissor
poetry install
````
3. Install simulator ([Description](software_guidebook/deployment.md))
4. Run the tool
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
