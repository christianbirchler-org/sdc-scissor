# SDC-Scissor tool for Cost-effective Simulation-based Test Selection in Self-driving Cars Software 

This project extends the tool competition platform from the [Cyber-Phisical Systems Testing Competition](https://github.com/se2p/tool-competition-av) which was part of the [SBST Workshop in 2021](https://sbst21.github.io/).

## SDC-Scissor Architecture

![Architecture Diagram](images/sdc-scissor-architecture.jpg)

## Usage

### Demo
[![Watch the video](https://img.youtube.com/vi/Cn8p648KnfQ/maxresdefault.jpg)](https://youtu.be/Cn8p648KnfQ)
[YouTube Link](https://youtu.be/Cn8p648KnfQ)

### Installation

The tool can either be run with [Docker](https://docs.docker.com/get-docker/) or locally using [Poetry](https://python-poetry.org/docs/).

When running the simulations a working installation of [BeamNG.research](https://beamng.gmbh/research/) is required.
Additionally this simulation cannot be run in a Docker container but must run locally.

To install the application use one of the following approaches:

* Docker: `docker build --tag sdc-scissor .`
* Poetry: `poetry install`

### Using the Tool

Sample test cases you can find here: https://doi.org/10.5281/zenodo.5914130

The tool can be used with the following two commands:

* Docker: `docker run --volume "$(pwd)/results:/out" --rm sdc-scissor [COMMAND] [OPTIONS]` (this will write all files written to `/out` to the local folder `results`)
* Poetry: `poetry run python sdc-scissor.py [COMMAND] [OPTIONS]`

There are multiple commands to use.
For simplifying the documentation only the command and their options are described.

* Generation of tests:
  * `generate-tests --out-path /path/to/store/tests`
* Automated labeling of Tests:
  * `label-tests --road-scenarios /path/to/tests --result-folder /path/to/store/labeled/tests`
  * *Note:* This only works locally with BeamNG.research installed
* Model evaluation:
  * `evaluate-models --dataset /path/to/train/set --save`
* Split train and test data:
  * `split-train-test-data --scenarios /path/to/scenarios --train-dir /path/for/train/data --test-dir /path/for/test/data --train-ratio 0.8`
* Test outcome prediction:
  * `predict-tests --scenarios /path/to/scenarios --classifier /path/to/model.joblib`
* Evaluation based on random strategy:
  * `evaluate --scenarios /path/to/test/scenarios --classifier /path/to/model.joblib`

The possible parameters are always documented with `--help`.

### Linting

The tool is verified the linters [flake8](https://flake8.pycqa.org/en/latest/) and [pylint](https://pylint.org).
These are automatically enabled in [Visual Studio Code](https://code.visualstudio.com) and can be run manually with the following commands:

```bash
poetry run flake8 .
poetry run pylint **/*.py
```

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
