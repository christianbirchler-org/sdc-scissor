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
pip install poetry
poetry install
````

## Install BeamNG.tech
For using SDC-Scissor with the BeamNG.tech simulator you can obtain an academic license from BeamNG from their
[website](https://register.beamng.tech/). After installing BeamNG.tech you need to replace the `tig` level it in the
user directory of BeamNG.tech (`C:\Users\myaccount\Documents\BeamNG.drive\0.24\levels`) wth the one from this repository
(`levels_template/tig`).


## Run the tool

A sample pipeline can be found with the following DOI: [10.24433/CO.1187310.v2](https://doi.org/10.24433/CO.1187310.v2)

### Sequence Diagram
```{mermaid}
sequenceDiagram
  actor User
  participant SDC-Scissor
  participant BeamNG.tech
  User ->> SDC-Scissor: Generate tests
  activate SDC-Scissor
  SDC-Scissor -->> User: Tests stored
  deactivate SDC-Scissor
  User ->> SDC-Scissor: Label tests
  activate BeamNG.tech
  loop for test in test suite
    SDC-Scissor ->> SDC-Scissor: Run test
    SDC-Scissor ->> BeamNG.tech: Run test in simulator
   end
  deactivate BeamNG.tech
  SDC-Scissor -->> User: Tests with outcome stored
  User ->> SDC-Scissor: Extract features
  SDC-Scissor -->> User: CSV file with features stored
  User ->> SDC-Scissor: Evaluate models
  SDC-Scissor -->> User: Trained models stored
  User ->> SDC-Scissor: Predict test outcome
  SDC-Scissor -->> User: Predicted test outcomes stored
  User ->> SDC-Scissor: Run only selected tests
  activate BeamNG.tech
  loop for test in selected tests
    SDC-Scissor ->> SDC-Scissor: Run test
    SDC-Scissor ->> BeamNG.tech: Run test in simulator
   end
  deactivate BeamNG.tech
  SDC-Scissor -->> User: Test outcomes stored
```

````shell
poetry run sdc-scissor -c sample_configs/label-tests.yml
````

The [Software Guidebook](../software_guidebook/introduction.md) provides more explanations about the
[installation](../software_guidebook/deployment.md) and [usage](../software_guidebook/operation_and_support.md) of
SDC-Scissor.

## Demo
````{note}
The following demo was made for SDC-Scissor v1.0. A demo video for the recent version is coming soon.
````

```{eval-rst}
..  youtube:: Cn8p648KnfQ
   :width: 695
   :height: 480
```

## Data
In the repository is a directory `sample_tests` with some simple sample test cases. These tests are mainly used for
development purposes.

The data used for the demo and evaluation of SDC-Scissor v1.0 we made available on Zenodo:
[![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.5903161.svg)](https://doi.org/10.5281/zenodo.5903161)
````{note}
The used simulator was BeamNG.research which is deprecated and not compatible anymore with SDC-Scissor.
````
