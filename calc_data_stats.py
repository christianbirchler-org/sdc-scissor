#!/bin/python3

import os
import sys
import json
import time
import re

if __name__ == '__main__':
    directory = sys.argv[1]
    abs_path_of_directory = os.path.abspath(directory)

    test_outcomes_lst = os.listdir(abs_path_of_directory)

    # test_generated, test_valid, test_invalid, test_passed, test_failed, test_in_error, real_time_execution, simulate_time_execution
    stats = {'test_generated': 0,
             'test_valid': 0,
             'test_invalid': 0,
             'test_passed': 0,
             'test_failed': 0}

    # define regex for relevant json files
    pattern = r"\d\d-\w\w\w-\d\d\d\d_\(\d\d-\d\d-\d\d\.\d*\)\.test\.\d\d\d\d\.json\Z"
    re_obj = re.compile(pattern)

    # traverse recursively through the directories provide by CLI
    for root, dirs, files in os.walk(abs_path_of_directory):
        # ignore a priori irrelevant folders
        if 'venv' in dirs:
            dirs.remove('venv')
        if 'simulations' in dirs:
            dirs.remove('simulations')  # don't visit CVS directories

        for file_name in files:
            # file is a json containing test outcome
            if re_obj.fullmatch(file_name):
                abs_path_of_test = os.path.join(root, file_name)

                # deserialize json
                test_outcome_json = None
                with open(abs_path_of_test, 'r') as file_obj:
                    test_outcome_json = json.load(file_obj)

                # update stats
                stats['test_generated'] += 1
                is_valid = test_outcome_json['is_valid']
                if is_valid:
                    stats['test_valid'] += 1
                else:
                    stats['test_invalid'] += 1
                    continue # there is no 'test_outcome' attribute!

                outcome = test_outcome_json['test_outcome']
                if outcome == 'PASS':
                    stats['test_passed'] += 1
                else:
                    stats['test_failed'] += 1

    print(str(stats))

