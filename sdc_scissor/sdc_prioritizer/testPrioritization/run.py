#!/usr/bin/env python
"""
Prioritize tests using NSGA-II
"""


import csv
from genericpath import exists
import sys
import os.path as path
import os
import numpy as np
import math


from crossover.PMX import PMXCrossover
from mutation.HybridMut import HybridMut
from problem.TestPrioritizationMultiObjectiveProblem import TestPrioritizationMultiObjectiveProblem

# pymoo libs
from pymoo.algorithms.moo.nsga2 import NSGA2

from pymoo.factory import get_sampling
from pymoo.optimize import minimize
from pymoo.util.display import MultiObjectiveDisplay
from pymoo.visualization.scatter import Scatter

# video recorder
from pyrecorder.recorder import Recorder
from pyrecorder.writers.video import Video

# sklearn
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler


MINIMUM_USER_INPTUS = 3
MAXIMUM_USER_INPTUS = 5


def fault_detection(X, lables, costs):
    length = len(lables)
    faults = np.array(lables)
    faults = np.where(faults == "safe", 0, faults)
    faults = np.where(faults == "unsafe", 1, faults).astype(float)

    x_values = np.zeros(length)
    y_values = np.zeros(length)

    total_faults = 0.0
    total_costs = 0.0

    for index in range(0, length):
        total_costs += costs[X[index]]
        total_faults += faults[X[index]]

        x_values[index] = total_costs
        y_values[index] = total_faults

    return x_values, y_values


def get_APFD(X, lables, costs):
    a, b = fault_detection(X, lables, costs)

    APFD = np.trapz(b, a) / (np.max(a) * np.max(b))
    print(f"APFD is {APFD}")
    return APFD


def get_costs_and_features(csv_file_path):
    costs = []
    features = []
    lables = []
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            costs.append(row[18])
            lables.append(row[19])
            features.append(row[:16])

    costs = np.array(costs).astype(float)
    features = np.array(features).astype(float)

    return costs, features, lables


def get_utopia(fitness_values):
    best_f1 = float("inf")
    best_f2 = float("inf")
    for fc in fitness_values:
        if fc[0] < best_f1:
            best_f1 = fc[0]
        if fc[1] < best_f2:
            best_f2 = fc[1]
    return [best_f1, best_f2]


def validate_user_input(user_input):
    # Check number of args
    if len(user_input) < MINIMUM_USER_INPTUS or len(user_input) > MAXIMUM_USER_INPTUS:
        print_help()
        exit()

    # Validate Features CSV file
    csv_file_path = user_input[0]

    if not path.exists(csv_file_path):
        print_help()
        exit()

    # Check configuration name
    config_name = user_input[1]
    if config_name == "":
        print_help()
        exit()

    output_dir = user_input[2]
    if not os.path.isdir(output_dir):
        print(f"{output_dir} is not a directory. Creating  {output_dir}")
        os.mkdir(output_dir)

    # check population size
    population_size = 100
    if len(user_input) >= 4:
        population_size = int(user_input[3])

    budget = 2000
    if len(user_input) == 5:
        budget = int(user_input[4])

    return csv_file_path, config_name, output_dir, population_size, budget


def print_help():
    """
    Print help text for wrong user input.
    """
    print(f"Expected at least {MINIMUM_USER_INPTUS} input arguments and at most {MAXIMUM_USER_INPTUS}.")
    print("arg 1 = Features CSV file path")
    print("arg 2 = Configuration name")
    print("arg 3 = Output directory")
    print("arg 4 (optional) = poulation size")
    print("arg 5 (optional) = number of generations")


def save_plot(output_dir, problem, res):
    plot = Scatter()
    plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    plot.add(res.F, facecolor="none", edgecolor="red")
    plot.save(path.join(output_dir, "plot.png"))


class MyDisplay(MultiObjectiveDisplay):
    def _do(self, problem, evaluator, algorithm):
        super()._do(problem, evaluator, algorithm)


def get_algorithm(algorithm, sampling_var, population_size=100):
    if algorithm == "NSGAII":
        return NSGA2(
            pop_size=population_size,
            sampling=sampling_var,
            crossover=PMXCrossover(),
            mutation=HybridMut(),
            eliminate_duplicates=True,
        )
    else:
        raise Exception("Unknown GA!")


def select_single_solution(res, scaler):
    normalized_solutions = scaler.fit_transform(res.F)
    print(normalized_solutions)

    best_solution = 0
    minimum_distance = float("inf")
    for index, solution_fitnesses in enumerate(normalized_solutions):
        f1 = solution_fitnesses[0]
        f2 = solution_fitnesses[1]
        distance = math.sqrt(f1**2 + f2**2)
        if distance < minimum_distance:
            minimum_distance = distance
            best_solution = index

    return best_solution


def save_solution(output_dir, solution):
    final_solution = solution.tolist()
    # print(final_solution)
    file_dir = os.path.join(output_dir, "solution.txt")
    # np.savetxt(file_dir, final_solution, fmt=str)
    textfile = open(file_dir, "w")
    for element in final_solution:
        textfile.write(str(element) + ", ")
    textfile.close


def main(user_input: list = None):
    cwd = os.getcwd()
    scaler = MinMaxScaler()

    """
    Main entry point when run the search process

    Args:
        user_input: argv[1]: Features CSV file path

    """
    # 1- Validating user inputs
    (csv_file_path, config_name, output_dir, population_size, budget) = validate_user_input(user_input)
    output_dir = os.path.join(output_dir, config_name)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    global costs
    # 2- Read CSV file
    costs, features, lables = get_costs_and_features(csv_file_path)
    genome_length = len(costs)

    # 3- Normalize all the features (min-max normalization)
    features = scaler.fit_transform(features)

    # 4- PCA
    pca = PCA()
    pca.fit(features)
    features = pca.transform(features)

    # 5- Compute the pairwse (Euclidean) distance between test cases
    global distances
    distances = np.sqrt(((features[:, :, None] - features[:, :, None].T) ** 2).sum(1))

    # 6- Run GA
    ## problem
    problem = TestPrioritizationMultiObjectiveProblem(genome_length, distances, costs)

    ## termination
    # termination = MultiObjectiveDefaultTermination(n_last=50, f_tol = 0)

    ## initialization (random solutions)
    sampling_var = get_sampling("perm_random")

    ## algorithm
    algorithm = get_algorithm("NSGAII", sampling_var, population_size)

    ## Start the search process
    res = minimize(problem, algorithm, ("n_gen", budget), save_history=False, display=MyDisplay(), verbose=True)

    ## 7 - print and save the outcome of the search process
    save_plot(output_dir, problem, res)

    # # use the video writer as a resource
    # with Recorder(Video(path.join(data_path,"ga.mp4"))) as rec:

    # # for each algorithm object in the history
    #     for entry in res.history:
    #         sc = Scatter(title=("Gen %s" % entry.n_gen))
    #         sc.add(entry.pop.get("F"))
    #         sc.add(entry.problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    #         sc.do()

    #         # finally record the current visualization to the video
    #         rec.record()

    # 8 - Select a solution
    best_solution_index = select_single_solution(res, scaler)

    print(f"Best solution has fitness values  {res.F[best_solution_index]}")

    final_solution = res.X[best_solution_index]
    final_solution_fitness = res.F[best_solution_index]

    # 9 - Save selected solution
    print(f"final_solution {final_solution.shape}")
    save_solution(output_dir, final_solution)

    # 9 - Calculate APFD
    get_APFD(final_solution, lables, costs)


if __name__ == "__main__":
    main(sys.argv[1:])
