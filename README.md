![example workflow](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/test.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ChristianBirchler_sdc-scissor)
[![](https://readthedocs.org/projects/sdc-scissor/badge)](https://sdc-scissor.readthedocs.io)

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=ChristianBirchler_sdc-scissor)

# SDC-Scissor tool for Cost-effective Simulation-based Test Selection in Self-driving Cars Software
SDC-Scissor is a tool that let you test self-driving cars more efficiently in simulation. It uses a machine-learning
approach to select only relevant test scenarios so that the testing process is faster. Furthermore, the selected tests
are diverse and try to challenge the car with corner cases.

Furthermore, this repository contains also code for test multi-objective test case prioritization with an evolutionary
genetic search algorithm. If you are interested in prioritizing test cases, then you should read the dedicated
[README.md](sdc_scissor/sdc_prioritizer/testPrioritization/README.md) for this.
If you use the prioritization technique then also cite the papers from the reference section!


## Docs

You find the documentation here: https://sdc-scissor.readthedocs.io


## Demo
[![Watch the video](https://img.youtube.com/vi/Cn8p648KnfQ/maxresdefault.jpg)](https://youtu.be/Cn8p648KnfQ)

[YouTube Link](https://youtu.be/Cn8p648KnfQ)

## Data
The data used for the demo and evaluation of SDC-Scissor v1.0 we made available on Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5903161.svg)](https://doi.org/10.5281/zenodo.5903161)

## Installation
The tool can either be run locally using [Poetry](https://python-poetry.org/docs/) (**RECOMMENDED**) or with [Docker](https://docs.docker.com/get-docker/).

When running the simulations a working installation of [BeamNG.tech](https://beamng.tech) is required.
Additionally, this simulation cannot be run in a Docker container but must run locally.

To install the SDC-Scissor, use one of the following approaches:

* Docker: `docker build --tag sdc-scissor .`
* Poetry: `poetry install`

## Usage
For SDC-Scissor v2.0 you can use the tests in the `sample_tests` directory.

The tool can be used with the following two commands:

* Docker: `docker run --volume "$(pwd)/destination:/var/project/destination" --rm sdc-scissor [COMMAND] [OPTIONS]` (this will write all files written to `/var/project/destination` to the local folder `destination`)
* Poetry: `poetry run python sdc-scissor.py [COMMAND] [OPTIONS]`

There are multiple commands to use.
For simplifying the documentation only the command and their options are described.

* Generation of tests:
  * `generate-tests`
* Extract the features into a CSV file:
  * `extract-features`
* Automated labeling of Tests:
  * `label-tests`
  * *Note:* This only works locally with BeamNG.research installed
* Model evaluation:
  * `evaluate-models`
* Evaluate the cost effectiveness of the models:
  * `evaluate_cost_effectiveness`
* Test outcome prediction:
  * `predict-tests`

The possible parameters are always documented with `--help`.

## License
The software we developed is distributed under GNU GPL license. See the [LICENSE.md](LICENSE.md) file.

## Contacts

Christian Birchler - Zurich University of Applied Science (ZHAW), Switzerland - birc@zhaw.ch

Nicolas Ganz - Zurich University of Applied Science (ZHAW), Switzerland - gann@zhaw.ch

Sajad Khatiri - Zurich University of Applied Science (ZHAW), Switzerland - mazr@zhaw.ch

Dr. Alessio Gambi  - Passau University, Germany - alessio.gambi@uni-passau.de

Dr. Sebastiano Panichella - Zurich University of Applied Science (ZHAW), Switzerland - panc@zhaw.ch

## References
**If you use this tool in your research, please cite the following papers:**

- Christian Birchler, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella. 2022. Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor. In 2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER), IEEE.
- Christian Birchler, Sajad Khatiri, Pouria Derakhshanfar, Sebastiano Panichella, and Annibale Panichella. 2022. Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments. ACM Transactions on Software Engineering and Methodology (TOSEM) (2022). DOI:https://doi.org/to appear

```{bibtex}
@INPROCEEDINGS{Birchler2022Cost,
  author={Birchler, Christian and Ganz, Nicolas and Khatiri, Sajad and Gambi, Alessio, and Panichella, Sebastiano},
  booktitle={2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER)},
  title={Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor},
  year={2022},
}

@article{Birchler2022Single,
  author = {Birchler, Christian and Khatiri, Sajad and Derakhshanfar, Pouria and Panichella, Sebastiano and Panichella, Annibale},
  title = {Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments},
  year = {2022},
  publisher = {Association for Computing Machinery},
  journal = {ACM Transactions on Software Engineering and Methodology (TOSEM)},
  doi = {to appear}
}
```
