import os
import subprocess
import json
import re
import random


SAMPLE_SIZE = 50
NR_TRIALS = 10
DATA_DIR = r'C:\Users\birc\Desktop\time-variance-analysis\data'
RESULTS_BASE_DIR = r'C:\Users\birc\Desktop\time-variance-analysis\results'
SIM_TIMES_DICT = {}


def _make_results_directory(trial):
    print('* make results directory')
    dir_name = 'trial_{}'.format(trial)
    if os.path.exists(RESULTS_BASE_DIR):
        print('exists')
    else:
        print('not existing')
    results_abs_path = os.path.join(RESULTS_BASE_DIR, dir_name)
    os.mkdir(results_abs_path)
    return results_abs_path


def _run_simulations(tests, result_dir):
    print('* run simulations')
    command = ['python', 'sdc-scissor.py', 'label-tests',
               '--tests', tests,
               '--labeled-tests', result_dir,
               '--risk-factor', '1.5',
               '--time-budget', '500000',
               '--oob-tolerance', '0.5',
               '--speed-limit', '120']

    subprocess.run(command, shell=True, check=True)


def _parse_json_test_file(file):
    print('* parse json test file {}'.format(file))
    json_dict = None
    with open(file, 'r') as file_obj:
        json_dict = json.load(file_obj)
    return json_dict


def _retrieve_sim_times(result_dir):
    print('* retrieve simulation times')
    pattern = r".*test.*\.json\Z"
    re_obj = re.compile(pattern)

    sim_times = []
    for root, _, files in os.walk(result_dir):
        for file in files:
            if re_obj.fullmatch(file):
                abs_file_path = os.path.join(root, file)
                json_dict = _parse_json_test_file(abs_file_path)
                sim_times.append(json_dict['simulation_time'])
    return sim_times


def _persist_sim_times():
    print('* persist simulation times to sim_times.json')
    file_path = os.path.join(RESULTS_BASE_DIR, 'sim_times.json')
    with open(file_path, 'w') as fp:
        json.dump(SIM_TIMES_DICT, fp)


def _write_sample_tests_to_dir(sample, sample_dir_name):
    print('* write sample tests to sample directory')
    for cnt, test in enumerate(sample):
        filename = 'sample_test_{}.json'.format(cnt)
        filepath = os.path.join(sample_dir_name, filename)
        with open(filepath, 'w') as fp:
            json.dump(test, fp)


def _random_sample_tests(size, stratified=False):
    print('* random sample tests')

    sample_dir_name = os.path.join(DATA_DIR, 'sample')
    if not os.path.exists(sample_dir_name):
        os.mkdir(sample_dir_name)

    pattern = r".*test.*\.json\Z"
    re_obj = re.compile(pattern)

    cnt_safe = 0
    cnt_unsafe = 0
    safe_tests_lst = []
    unsafe_tests_lst = []
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if re_obj.fullmatch(file):
                abs_file_path = os.path.join(root, file)
                json_dict = _parse_json_test_file(abs_file_path)
                test_is_valid = json_dict['is_valid']
                if test_is_valid:
                    test_outcome = json_dict['test_outcome']
                    if test_outcome == 'PASS':
                        safe_tests_lst.append(json_dict)
                        cnt_safe += 1
                    elif test_outcome == 'FAIL':
                        unsafe_tests_lst.append(json_dict)
                        cnt_unsafe += 1

    random.shuffle(safe_tests_lst)
    random.shuffle(unsafe_tests_lst)
    sample = []
    if stratified:
        group_size = size//2
        if cnt_safe < group_size:
            raise Exception('Not enough safe tests for the sample!')
        if cnt_unsafe < group_size:
            raise Exception('Not enough unsafe tests for the sample!')

        sample += random.sample(safe_tests_lst, group_size)
        sample += random.sample(unsafe_tests_lst, group_size)
    else:
        sample += safe_tests_lst
        sample += unsafe_tests_lst
        random.shuffle(sample)
        sample = random.sample(sample, size)
    random.shuffle(sample)

    _write_sample_tests_to_dir(sample, sample_dir_name)

    return sample_dir_name


def main():
    print('* start script')
    sample_dir = _random_sample_tests(SAMPLE_SIZE, stratified=True)
    for trial in range(NR_TRIALS):
        print('* Trial {}'.format(trial))
        result_dir = _make_results_directory(trial)
        _run_simulations(sample_dir, result_dir)
        sim_times = _retrieve_sim_times(result_dir)
        key = 'trial_{}'.format(trial)
        SIM_TIMES_DICT[key] = sim_times
    _persist_sim_times()


if __name__ == '__main__':
    main()
