# SDC-Scissor tool for Cost-effective Simulation-based Test Selection in Self-driving Cars Software

This project extends the tool competition platform from the [Cyber-Phisical Systems Testing Competition](https://github.com/se2p/tool-competition-av) which was part of the [SBST Workshop in 2021](https://sbst21.github.io/).

## SDC-Scissor Architecture
![Architecture Diagram](images/sdc-scissor-architecture.jpg)

## SDC-Scissor Components and APIs
![Component Diagram](images/sdc-scissor-APIs.jpg)

## Usage

### Demo
[![Watch the video](https://img.youtube.com/vi/Cn8p648KnfQ/maxresdefault.jpg)](https://youtu.be/Cn8p648KnfQ)
[YouTube Link](https://youtu.be/Cn8p648KnfQ)

### Data
The data used for the demo and evaluation of SDC-Scissor v1.0 we made available on Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5903161.svg)](https://doi.org/10.5281/zenodo.5903161)


### Installation

The tool can either be run locally using [Poetry](https://python-poetry.org/docs/) (**RECOMMENDED**) or with [Docker](https://docs.docker.com/get-docker/).

When running the simulations a working installation of [BeamNG.tech](https://beamng.tech) is required.
Additionally, this simulation cannot be run in a Docker container but must run locally.

To install the SDC-Scissor, use one of the following approaches:

* Docker: `docker build --tag sdc-scissor .`
* Poetry: `poetry install`

### Using the Tool

Sample test cases for SDC-Scissor v1.0 you can find here: https://doi.org/10.5281/zenodo.5914130

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
- Christian Birchler, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella. 2022. Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor. In 2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER), IEEE.

**If you use this tool in your research, please cite the following papers:**
```
@INPROCEEDINGS{Birchler2022,
  author={Birchler, Christian and Ganz, Nicolas and Khatiri, Sajad and Gambi, Alessio, and Panichella, Sebastiano},
  booktitle={2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER),
  title={Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor},
  year={2022},
}
```
