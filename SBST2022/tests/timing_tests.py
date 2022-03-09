import unittest
from click.testing import CliRunner
from competition import generate
from unittest.mock import patch
import tempfile

class TimingTest(unittest.TestCase):

    # def get_script_path():
    #     return os.path.dirname(os.path.realpath(sys.argv[0]))

    def test_total_time(self):
        with patch('competition.get_script_path', return_value=tempfile.mkdtemp()):
            runner = CliRunner()
            result = runner.invoke(generate,
                               ['--executor', 'mock', '--time-budget', '20', '--map-size', '200',
                                '--module-path', '..',
                                '--module-name',
                                'sample_test_generators.random_generator', '--class-name', 'RandomTestGenerator'])
            output = result.output
            print(output)
            print(">> Exit code is ", result.exit_code)
            # 123 indicates that the budget for the execution was completely consumed DURING the testing
            # 0 indicates that the budget for the execution was completely consumed IN BETWEEN test generation and execution
            assert result.exit_code == 123 or result.exit_code == 0
            # assert result.exit_code == 0

    def test_with_generation_and_execution_times(self):
        with patch('competition.get_script_path', return_value=tempfile.mkdtemp()):
            runner = CliRunner()
            # Execution should allow max 2 simulated tests, each taking 3.0 seconds (mock executor)
            result = runner.invoke(generate,
                                   ['--executor', 'mock', '--generation-budget', '10', '--execution-budget', '7' 
                                    '--map-size', '200',
                                    '--module-path', '..',
                                    '--module-name',
                                    'sample_test_generators.random_generator', '--class-name', 'RandomTestGenerator'])
            output = result.output
            print(output)
            print(">> Exit code is ", result.exit_code)
            # 123 indicates that the budget for the execution was completely consumed
            assert result.exit_code == 123
            # assert result.exit_code == 0

