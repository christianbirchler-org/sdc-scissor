"""
Usage: poetry run python transform_results.py [FOLDER WITH TEST RUNS]
Expects a folder like:
- run1/
    - some_run_file.json
    - some_other_run_file.json
    - ...
    - simulations/
        - beamng_executor/
            - some_simulation_folder/
                - simulation.full.json
            - some_other_simulation_folder/
                - simulation.full.json
- run2/
    - ...
- ...

Only the "simulations", "beamng_executor" and "simulation.full.json" files/folders must be named correctly
others are determined from the structure
"""

import sys
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Any, List


def _transform_run(folder: Path) -> None:
    simulations_folder = folder / 'simulations' / 'beamng_executor'
    if not simulations_folder.exists():
        _abort(f'Simulation folder {simulations_folder} does not exist')
    simulations = list(sorted(simulations_folder.glob('*/simulation.full.json')))
    # reverse the lists to use the more efficient .pop()
    simulations.reverse()
    test_files = sorted(folder.glob('*.json'))

    transformed_folder = folder / 'transformed'
    if transformed_folder.exists():
        shutil.rmtree(transformed_folder)

    transformed_folder.mkdir()

    for test_file in test_files:
        test_data = _read_json(test_file)
        test_data['duration'] = _get_duration(test_data, simulations)
        _write_json(transformed_folder / test_file.name, test_data)

    if len(simulations) != 0:
        _abort('too many simulations for test runs')

    print(f'Wrote {len(test_files)} tests to {transformed_folder}')


def _transform_results(folder: Path) -> None:
    if not folder.exists():
        _abort(f'{folder} does not exist')

    for result_folder in folder.iterdir():
        if result_folder.is_dir():
            _transform_run(result_folder)


def _abort(msg: str) -> None:
    print('ERROR:', msg)
    sys.exit(1)


def _read_json(path: Path) -> Any:
    with path.open('r') as fp:
        return json.load(fp)


def _write_json(path: Path, obj: Any) -> None:
    with path.open('w') as fp:
        json.dump(obj, fp)


def _get_duration(test_data: Any, simulations: List[Path]) -> float:
    if not test_data['is_valid']:
        return -1

    if len(simulations) == 0:
        _abort('Not enough simulations for the test files')
    simulation_data = _read_json(simulations.pop())
    start_time = datetime.fromisoformat(simulation_data['info']['start_time'])
    end_time = datetime.fromisoformat(simulation_data['info']['end_time'])
    return (end_time - start_time).total_seconds()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        _abort('exactly one parameter is required')
    _transform_results(Path(sys.argv[1]))
