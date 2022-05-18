# Python Test Prioritizer
 This tool gets the information regarding the tests written for self-driving cars and performs an evolutionary algorithm to deliver a test execution order that captures more unsafe behavior with less test execution time.

## Getting Started

1- Clone this repository.

2- Build the docker image:
```bash
. docker_scripts/build-test-prioritization-image.sh 
```

3- Run the docker container:
```bash
. docker_scripts/run-test-prioritization-container.sh
```

4- Run the Test Prioritizer:

```bash
docker exec -it test-prioritization-container bash -c "python testPrioritization/run.py <dataset CSV file> <execution name> <output directory> [population size] [number of generations]"
```
This script has minimum __3__ and maximum __5__ input parameters. We will explain each of these arguments here:

ARG1) __dataset CSV file:__ The address to one of the CSV files including all of the features in a set of tests.

ARG2) __execution name:__ Each execution should have a unique name. The prioritizer stores all of the outputs under a directory with this name.

ARG3) __output directory:__ The prioritizer stores all of the outputs in this directory. If the given directory does not exist, the script will create it. The processor will create a subdirectory with the given `<execution name>` in the given `<output directory>`.

ARG4) __population size__ (optional)__:__ This argument indicates the number of solutions that the genetic algorithm produces in each generation. This value is set to 100 by default.

ARG5) __number of generations__ (optional)__:__ This argument indicates the search budget of the prioritizer. This value is set to 2000. It means that The search process stops after generating the 2000th generation of test orders by default.
### Outputs 
The search process saves the Pareto front as `plot.png` in the output directory. It also saves the best-generated test order as `solution.txt` in the same directory.
### Example 
For example, the following command will execute the test prioritization for `BeamNG_RF_1_Complete` dataset with a population size of 50 and a search budget of 1000 generations. The output of this process will be saved under `data/results/config1`:


```bash
docker exec -it test-prioritization-container bash -c "python testPrioritization/run.py datasets/fullroad/BeamNG_AI/BeamNG_RF_1/BeamNG_RF_1_Complete.csv 'config1' data/results/ 50 1000"
```