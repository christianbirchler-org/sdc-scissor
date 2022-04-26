Usage
=====

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
