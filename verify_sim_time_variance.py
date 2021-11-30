import os
import subprocess
import json
import re


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


def _run_simulations(result_dir):
    print('* run simulations')
    command = ['python', 'sdc-scissor.py', 'label-tests',
               '--tests', DATA_DIR,
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


def _sample_tests():
    pass


def main():
    print('* start script')
    tests = _sample_tests()
    for trial in range(NR_TRIALS):
        print('* Trial {}'.format(trial))
        result_dir = _make_results_directory(trial)
        _run_simulations(result_dir)
        sim_times = _retrieve_sim_times(result_dir)
        key = 'trial_{}'.format(trial)
        SIM_TIMES_DICT[key] = sim_times
    _persist_sim_times()


if __name__ == '__main__':
    main()
