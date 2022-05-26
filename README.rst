.. image:: https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/pipeline.yml/badge.svg
    :target: https://github.com/ChristianBirchler/sdc-scissor/actions

.. image:: https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=alert_status
    :target: https://sonarcloud.io/summary/new_code?id=ChristianBirchler_sdc-scissor

.. image:: https://readthedocs.org/projects/sdc-scissor/badge
    :target: https://sdc-scissor.readthedocs.io

SDC-Scissor tool for Cost-effective Simulation-based Test Selection in Self-driving Cars Software
=================================================================================================
.. image:: https://sonarcloud.io/images/project_badges/sonarcloud-white.svg
    :target: https://sonarcloud.io/summary/new_code?id=ChristianBirchler_sdc-scissor

SDC-Scissor is a tool that let you test self-driving cars more efficiently in simulation. It uses a machine-learning
approach to select only relevant test scenarios so that the testing process is faster. Furthermore, the selected tests
are diverse and try to challenge the car with corner cases.

Furthermore, this repository contains also code for test multi-objective test case prioritization with an evolutionary
genetic search algorithm. If you are interested in prioritizing test cases, then you should read the dedicated
`README.md <https://github.com/ChristianBirchler/sdc-scissor/blob/main/sdc_scissor/sdc_prioritizer/testPrioritization/README.md>`_ for this.
If you use the prioritization technique then also cite the papers from the reference section!


Documentation
-------------
.. image:: https://raw.githubusercontent.com/ChristianBirchler/sdc-scissor/main/docs/readthedocs.png
    :target: https://sdc-scissor.readthedocs.io/en/latest/

License
-------
.. code-block:: text

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

The software we developed is distributed under GNU GPL license. See the `LICENSE.md <https://github.com/ChristianBirchler/sdc-scissor/blob/main/LICENSE.md>`_ file.

References
----------
**If you use this tool in your research, please cite the following papers:**

- Christian Birchler, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella. 2022. Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor. In 2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER), IEEE.
- Christian Birchler, Sajad Khatiri, Pouria Derakhshanfar, Sebastiano Panichella, and Annibale Panichella. 2022. Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments. ACM Transactions on Software Engineering and Methodology (TOSEM) (2022). DOI: to appear


.. code-block:: latex

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

Contacts
--------
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
