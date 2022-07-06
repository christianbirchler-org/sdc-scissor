# SDC-Scissor
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/ci.yml/badge.svg)](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/ci.yml)
[![CD](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/cd.yml/badge.svg)](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/cd.yml)
[![](https://readthedocs.org/projects/sdc-scissor/badge)](https://sdc-scissor.readthedocs.io)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=alert_status)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=ncloc)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=coverage)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=sqale_index)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=reliability_rating)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=duplicated_lines_density)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=vulnerabilities)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=bugs)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=security_rating)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=sqale_rating)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)
[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=code_smells)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)

## A Tool for Cost-effective Simulation-based Test Selection in Self-driving Cars Software
<div style="text-align: center;">
<a href="https://github.com/ChristianBirchler/sdc-scissor">
<img src="https://raw.githubusercontent.com/ChristianBirchler/sdc-scissor/main/docs/images/github_logo_icon.png">
</a>
<a href="https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor">
<img src="https://sonarcloud.io/images/project_badges/sonarcloud-black.svg">
</a>
</div>

SDC-Scissor is a tool that let you test self-driving cars more efficiently in simulation. It uses a machine-learning
approach to select only relevant test scenarios so that the testing process is faster. Furthermore, the selected tests
are diverse and try to challenge the car with corner cases.

Furthermore, this repository contains also code for test multi-objective test case prioritization with an evolutionary
genetic search algorithm. If you are interested in prioritizing test cases, then you should read the dedicated
[README.md](https://github.com/ChristianBirchler/sdc-scissor/blob/main/sdc_scissor/sdc_prioritizer/testPrioritization/README.md)
for this. If you use the prioritization technique then also cite the papers from the reference section!

## Support
Join the community on [Slack](https://slack.com/) or [Discord](https://discord.com/) to get support of developers and
users. Just click on one of the following links:

* [https://join.slack.com/t/sdc-scissor/shared_invite/zt-1aikrj1uu-Dz0a9BE1AQ4GQp4A3Bm5og](https://join.slack.com/t/sdc-scissor/shared_invite/zt-1aikrj1uu-Dz0a9BE1AQ4GQp4A3Bm5og)
* [https://discord.gg/AaYnBS6s7E](https://discord.gg/AaYnBS6s7E)

## Documentation
[![](https://raw.githubusercontent.com/ChristianBirchler/sdc-scissor/main/docs/images/readthedocs.png)](https://sdc-scissor.readthedocs.io/en/latest/)

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

* Christian Birchler, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella. 2022. Cost-effective
Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor. In 2022 IEEE 29th International
Conference on Software Analysis, Evolution and Reengineering (SANER), IEEE.

* Christian Birchler, Sajad Khatiri, Pouria Derakhshanfar, Sebastiano Panichella, and Annibale Panichella. 2022.
Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments. ACM Transactions on
Software Engineering and Methodology (TOSEM) (2022). DOI: to appear

```{code-block} bibtex
@inproceedings{Birchler2022Cost,
  author={Birchler, Christian and Ganz, Nicolas and Khatiri, Sajad and Gambi, Alessio, and Panichella, Sebastiano},
  booktitle={2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER)},
  title={Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor},
  year={2022},
  doi={to appear}
}

@article{Birchler2022Single,
  author={Birchler, Christian and Khatiri, Sajad and Derakhshanfar, Pouria and Panichella, Sebastiano and Panichella, Annibale},
  title={Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments},
  year={2022},
  publisher={Association for Computing Machinery},
  journal={ACM Transactions on Software Engineering and Methodology (TOSEM)},
  doi={to appear}
}
```

## Contacts
* Christian Birchler
    * Zurich University of Applied Science (ZHAW), Switzerland - birc@zhaw.ch
* Nicolas Ganz
    * Zurich University of Applied Science (ZHAW), Switzerland - gann@zhaw.ch
* Sajad Khatiri
    * Zurich University of Applied Science (ZHAW), Switzerland - mazr@zhaw.ch
* Dr. Alessio Gambi
    * Passau University, Germany - alessio.gambi@uni-passau.de
* Dr. Sebastiano Panichella
    * Zurich University of Applied Science (ZHAW), Switzerland - panc@zhaw.ch
