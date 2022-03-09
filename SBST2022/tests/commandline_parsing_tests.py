import unittest
from click.testing import CliRunner
from time import sleep
from competition import generate

# FOR SOME REASONS THOSE TESTS WORK ONLY IF WE START ONE AFTER THE OTHER MANUALLY
# I suspect this might be because we exended the Command class from click
class CommandLineCombinationTest(unittest.TestCase):

    def test_fail_when_model_is_missing(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--executor', 'dave2', '--time-budget', '10', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Error: If executor is set to dave2 the option --dave2-model must be specified" in output, output

    def test_do_not_fail_when_model_is_missing_but_executor_is_different(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--executor', 'mock', '--time-budget', '10', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Started test generation" in output, output

    def test_do_fail_when_model_is_present_but_executor_is_different(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--executor', 'mock', '--dave2-model', '../dave2/self-driving-car-010-2020.h5', '--time-budget', '10', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Started test generation" in output, output

    def test_do_not_fail_when_model_is_present(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--executor', 'dave2', '--dave2-model', '../dave2/self-driving-car-010-2020.h5', '--time-budget', '10', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Started test generation" in output, output


class TimeBudgetCombinationTest(unittest.TestCase):

    def test_fail_when_none_is_defined(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--executor', 'mock', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Error: At least one of those options must be defined ['--time-budget', '--generation-budget', '--execution-budget']" in output, output

    def test_do_not_fail_when_time_budget_is_defined(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--time-budget', '10', '--executor', 'mock', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Started test generation" in output, output

    def test_do_not_fail_when_generation_and_execution_budgets_are_defined(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--generation-budget', '10', '--execution-budget', '20', '--executor', 'mock', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Started test generation" in output, output

    def test_fail_when_all_are_defined(self):
        runner = CliRunner()
        result = runner.invoke(generate, ['--time-budget', '10', '--generation-budget', '10', '--execution-budget', '20', '--executor', 'mock', '--map-size', '200', '--module-name', 'foo', '--class-name', 'Foo'])
        output = result.output
        assert "Error: Only one of those options must be defined" in output, output