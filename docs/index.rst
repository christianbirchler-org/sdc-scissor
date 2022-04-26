.. SDC-Scissor documentation master file, created by
   sphinx-quickstart on Mon Apr 25 10:49:01 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SDC-Scissor's documentation!
=======================================
SDC-Scissor is a tool that let you test self-driving cars more efficiently in simulation. It uses a machine-learning
approach to select only relevant test scenarios so that the testing process is faster. Furthermore, the selected tests
are diverse and try to challenge the car with corner cases.

Content
-------
.. toctree::
   :maxdepth: 2

   demo
   installation
   usage
   data
   api

SDC-Scissor Architecture
------------------------
.. image:: ../images/sdc-scissor-architecture.jpg

SDC-Scissor Components and APIs
-------------------------------
.. image:: ../images/sdc-scissor-APIs.jpg

License
-------
The software we developed is distributed under GNU GPL license. See the `LICENSE.md <https://github.com/ChristianBirchler/sdc-scissor/blob/main/LICENSE.md>`_ file.

Contacts
--------
- Christian Birchler - Zurich University of Applied Science (ZHAW), Switzerland - birc@zhaw.ch
- Nicolas Ganz - Zurich University of Applied Science (ZHAW), Switzerland - gann@zhaw.ch
- Sajad Khatiri - Zurich University of Applied Science (ZHAW), Switzerland - mazr@zhaw.ch
- Dr. Alessio Gambi  - Passau University, Germany - alessio.gambi@uni-passau.de
- Dr. Sebastiano Panichella - Zurich University of Applied Science (ZHAW), Switzerland - panc@zhaw.ch

References
----------
**If you use this tool in your research, please cite the following papers:**

- Christian Birchler, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella. 2022. Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor. In 2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER), IEEE.

.. code-block:: bibtex

   @INPROCEEDINGS{Birchler2022,
     author={Birchler, Christian and Ganz, Nicolas and Khatiri, Sajad and Gambi, Alessio, and Panichella, Sebastiano},
     booktitle={2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER)},
     title={Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor},
     year={2022},
   }
