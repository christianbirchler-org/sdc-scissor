import random
from pathlib import Path

from sdc_scissor.testing_api.test_generator import TestGenerator, KeepAllTestsBehavior, KeepValidTestsOnlyBehavior
from sdc_scissor.testing_api.test_validator import SimpleTestValidator, MakeTestInvalidValidator


class TestTestGenerator:
    def test_id_generation_of_generate_tests_on_keeping_all_tests(self, mocker, fs):
        destination = "./destination"
        number_of_tests_to_generate = 10
        tool = "frenetic"
        destination = Path(destination)
        if not destination.exists():
            destination.mkdir(parents=True)

        test_keeping_behavior = KeepAllTestsBehavior()
        test_validator = MakeTestInvalidValidator(SimpleTestValidator())
        test_generator = TestGenerator(
            count=number_of_tests_to_generate,
            destination=destination,
            tool=tool,
            validator=test_validator,
            test_keeping_behavior=test_keeping_behavior,
        )
        test_generator.generate()

        expected = number_of_tests_to_generate
        actual = len(test_generator.generated_tests)
        assert actual == expected
        for index, test in enumerate(test_generator.generated_tests):
            expected = index
            actual = test.test_id
            assert expected == actual

    def test_id_generation_of_generate_tests_on_keeping_valid_tests_only(self, fs):
        random.seed(9)  # With this seed (seed=9 ==> 3 invalid tests) we get three invalid test generated.
        destination = "./destination"
        number_of_tests_to_generate = 100
        tool = "frenetic"
        destination = Path(destination)
        if not destination.exists():
            destination.mkdir(parents=True)

        test_keeping_behavior = KeepValidTestsOnlyBehavior()
        test_validator = SimpleTestValidator()
        test_generator = TestGenerator(
            count=number_of_tests_to_generate,
            destination=destination,
            tool=tool,
            validator=test_validator,
            test_keeping_behavior=test_keeping_behavior,
        )
        test_generator.generate()
        for index, test in enumerate(test_generator.generated_tests):
            expected = index
            actual = test.test_id
            assert expected == actual
