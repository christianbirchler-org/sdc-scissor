# SDC-Scissor
```{code-block} text
 ____    ____    ____              ____
/\  _`\ /\  _`\ /\  _`\           /\  _`\           __
\ \,\L\_\ \ \/\ \ \ \/\_\         \ \,\L\_\    ___ /\_\    ____    ____    ___   _ __
 \/_\__ \\ \ \ \ \ \ \/_/_  _______\/_\__ \   /'___\/\ \  /',__\  /',__\  / __`\/\`'__\
   /\ \L\ \ \ \_\ \ \ \L\ \/\______\ /\ \L\ \/\ \__/\ \ \/\__, `\/\__, `\/\ \L\ \ \ \/
   \ `\____\ \____/\ \____/\/______/ \ `\____\ \____\\ \_\/\____/\/\____/\ \____/\ \_\
    \/_____/\/___/  \/___/            \/_____/\/____/ \/_/\/___/  \/___/  \/___/  \/_/


```
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![GitHub issues](https://img.shields.io/github/issues/ChristianBirchler/sdc-scissor)](https://github.com/christianbirchler-org/sdc-scissor/issues)
[![GitHub forks](https://img.shields.io/github/forks/ChristianBirchler/sdc-scissor)](https://github.com/christianbirchler-org/sdc-scissor/network)
[![GitHub stars](https://img.shields.io/github/stars/ChristianBirchler/sdc-scissor)](https://github.com/christianbirchler-org/sdc-scissor/stargazers)
[![](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/ci.yml/badge.svg)](https://github.com/christianbirchler-org/sdc-scissor/actions/workflows/ci.yml)
[![CD](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/cd.yml/badge.svg)](https://github.com/christianbirchler-org/sdc-scissor/actions/workflows/cd.yml)
[![PyPI](https://img.shields.io/pypi/v/sdc-scissor)](https://pypi.org/project/sdc-scissor/)
[![](https://readthedocs.org/projects/sdc-scissor/badge)](https://sdc-scissor.readthedocs.io)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=alert_status)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=ncloc)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=coverage)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=sqale_index)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=reliability_rating)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=duplicated_lines_density)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=vulnerabilities)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=bugs)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=security_rating)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=sqale_rating)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=christianbirchler-org_sdc-scissor&metric=code_smells)](https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor)
[![DOI](https://zenodo.org/badge/363107094.svg)](https://zenodo.org/badge/latestdoi/363107094)
<div style="text-align: center;">
<a href="https://github.com/christianbirchler-org/sdc-scissor">
<img src="https://raw.githubusercontent.com/christianbirchler-org/sdc-scissor/main/docs/images/github_logo_icon.png">
</a>
<a href="https://sonarcloud.io/summary/overall?id=christianbirchler-org_sdc-scissor">
<img src="https://sonarcloud.io/images/project_badges/sonarcloud-black.svg">
</a>
</div>

## A Tool for Cost-effective Simulation-based Test Selection in Self-driving Cars Software
SDC-Scissor is a tool that let you test self-driving cars more efficiently in simulation. It uses a machine-learning
approach to select only relevant test scenarios so that the testing process is faster. Furthermore, the selected tests
are diverse and try to challenge the car with corner cases.

Furthermore, this repository contains also code for test multi-objective test case prioritization with an evolutionary
genetic search algorithm. If you are interested in prioritizing test cases, then you should read the dedicated
[README.md](https://github.com/christianbirchler-org/sdc-scissor/blob/main/sdc_scissor/sdc_prioritizer/testPrioritization/README.md)
for this. If you use the prioritization technique then also cite the papers from the reference section!

## Support
We use [GitHub Discussions](https://github.com/christianbirchler-org/sdc-scissor/discussions) as a community platform. You
can ask questions and get support there from the community. Furthermore, new features and releases will be discussed and
announced there.

## Documentation
For the documentation follow the link: [sdc-scissor.readthedocs.io](https://sdc-scissor.readthedocs.io/en/latest/)

[![](https://raw.githubusercontent.com/christianbirchler-org/sdc-scissor/main/docs/images/readthedocs.png)](https://sdc-scissor.readthedocs.io/en/latest/)

## License
```{code-block} text
SDC-Scissor tool for cost-effective simulation-based test selection
in self-driving cars software.
Copyright (C) 2022  Christian Birchler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

The software we developed is distributed under GNU GPL license. See the
[LICENSE.md](https://github.com/ChristianBirchler/sdc-scissor/blob/main/LICENSE.md) file.

## References
If you use this tool in your research, please cite the following papers:

- **Christian Birchler**, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella, "Cost-effective Simulation-based Test Selection in Self-driving Cars Software with SDC-Scissor," *In 2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER)*, pp. 164-168, doi: 10.1109/SANER53432.2022.00030.
  - [IEEE Xplore](https://doi.org/10.1109/SANER53432.2022.00030)
  - [Preprint](https://doi.org/10.21256/zhaw-24017)
  - [GitHub](https://github.com/ChristianBirchler/sdc-scissor)
````{code-block} bibtex
@inproceedings{Birchler2022Cost1,
  author={Birchler, Christian and Ganz, Nicolas and Khatiri, Sajad and Gambi, Alessio, and Panichella, Sebastiano},
  booktitle={2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER)},
  title={Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor},
  year={2022},
  doi={10.1109/SANER53432.2022.00030}
}
````
- **Christian Birchler**, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella, "Cost-effective Simulation-based Test Selection in Self-driving Cars Software," *Science of Computer Programming (SCP)*, doi: 10.1016/j.scico.2023.102926, 2023.
  - [Elsevier](https://doi.org/10.1016/j.scico.2023.102926)
````{code-block} bibtex
@article{Birchler2022Cost2,
  author    = {Christian Birchler and Nicolas Ganz and Sajad Khatiri and Alessio Gambi and Sebastiano Panichella},
  title     = {Cost-effective Simulation-based Test Selection in Self-driving Cars Software},
  journal   = {Science of Computer Programming (SCP)},
  volume    = {226},
  year      = {2023},
  doi       = {10.1016/j.scico.2023.102926},
  pages     = {102926},
  year      = {2023},
  issn      = {0167-6423},
}
````
- **Christian Birchler**, Sajad Khatiri, Bill Bosshard, Alessio Gambi, and Sebastiano Panichella, "Machine Learning-based Test Selection for Simulation-based Testing of Self-driving Cars Software," *Empirical Software Engineering (EMSE)*, doi: to appear, 2022.
  - [Preprint](https://doi.org/10.48550/arXiv.2212.04769)
````{code-block} bibtex
@article{Birchler2022Machine,
  author    = {Christian Birchler and Sajad Khatiri and Bill Bosshard and Alessio Gambi and Sebastiano Panichella},
  title     = {Machine Learning-based Test Selection for Simulation-based Testing of Self-driving Cars Software},
  journal   = {Empirical Software Engineering (EMSE)},
  year      = {2022},
  doi       = {to appear},
  eprinttype = {arXiv},
  eprint    = {2212.04769}
}
````
- **Christian Birchler**, Sajad Khatiri, Pouria Derakhshanfar, Sebastiano Panichella, and Annibale Panichella, "Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments," *ACM Transactions on Software Engineering and Methodology (TOSEM)*, doi: 10.1145/3533818, 2022.
  - [ACM Digital Library](https://doi.org/10.1145/3533818)
  - [Preprint](https://doi.org/10.48550/arXiv.2107.09614)
```{code-block} bibtex
@article{Birchler2022Single,
  author={Birchler, Christian and Khatiri, Sajad and Derakhshanfar, Pouria and Panichella, Sebastiano and Panichella, Annibale},
  title={Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments},
  year={2022},
  publisher={Association for Computing Machinery},
  journal={ACM Transactions on Software Engineering and Methodology (TOSEM)},
  doi={10.1145/3533818}
}
```

## Contacts
* Christian Birchler
    * Zurich University of Applied Sciences (ZHAW), Switzerland - birc@zhaw.ch
* Nicolas Ganz
    * Zurich University of Applied Sciences (ZHAW), Switzerland - gann@zhaw.ch
* Sajad Khatiri
    * Zurich University of Applied Sciences (ZHAW), Switzerland - mazr@zhaw.ch
* Dr. Alessio Gambi
    * IMC University Of Applied Sciences Krems, Austria - alessio.gambi@fh-krems.ac.at
* Dr. Sebastiano Panichella
    * Zurich University of Applied Sciences (ZHAW), Switzerland - panc@zhaw.ch
