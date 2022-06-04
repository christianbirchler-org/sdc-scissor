Installation
============
The tool can either be run locally using `Poetry <https://python-poetry.org/docs/>`_ (**RECOMMENDED**) or with
`Docker <https://docs.docker.com/get-docker/>`_.

Requirements
------------
* BeamNG
    * When running the simulations a working installation of `BeamNG.tech <https://beamng.tech>`_ is required.
    * Additionally, this simulation cannot be run in a ``Docker`` container but must run locally.
* ``Python 3.9``
    * Note: ``SDC-Scissor`` is tested with this version of python only
* `Poetry <https://python-poetry.org/docs/>`_
* `Docker <https://docs.docker.com/get-docker/>`_

Installation commands
---------------------
To install the ``SDC-Scissor``, use one of the following approaches:

* Docker: ``docker build --tag sdc-scissor .``
* Poetry: ``poetry install``
