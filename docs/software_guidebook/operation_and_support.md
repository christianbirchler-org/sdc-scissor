# Operation and Support
This section provides information about the operational and support aspects of SDC-Scissor.


## Usage
For SDC-Scissor v2.0 you can use the tests in the `sample_tests` directory.

The tool can be used with the following two commands:

* PyPI: `sdc-scissor [COMMAND] [OPTIONS]`
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

## Community
We want to set up a community of researchers, developers, and users of SDCs. To enhance the research on these topics, we
use the platform on [GitHub Discussions](https://github.com/ChristianBirchler/sdc-scissor/discussions) as the main
communication channel to discuss everything related on SDCs and SDC-Scissor. Feel free to join the discussions if you
want to discuss new potential features that can be implemented or research ideas. Everyone is welcome!

For more detailed information about contributing to SDC-Scissor, please refer to
[CONTRIBUTING.md](../../CONTRIBUTING.md).
