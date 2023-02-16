from sdc_scissor.testing_api.test_validator import NoIntersectionValidator
from sdc_scissor.testing_api.test_validator import NoTooSharpTurnsValidator
from sdc_scissor.testing_api.test_validator import SimpleTestValidator
from sdc_scissor.testing_api.test_validator import Test


class TestTestValidator:
    def test_simple_test_validator(self, mocker):
        test = mocker.patch("sdc_scissor.testing_api.test_validator.Test")
        tv = SimpleTestValidator()
        expected = True
        actual = tv.validate(test)
        assert actual == expected

    def test_no_intersection_decorator_on_valid_test(self):
        test = Test(0, road_points=[[10, 10], [15, 15], [100, 100], [150, 150]], test_outcome=None, test_duration=None)
        tv = NoIntersectionValidator(SimpleTestValidator())
        expected = True
        actual = tv.validate(test)
        assert actual == expected

    def test_no_intersection_decorator_on_invalid_test(self):
        test = Test(
            0,
            road_points=[[10, 10], [100, 10], [150, 50], [100, 100], [60, 60], [20, 0], [20, -10]],
            test_outcome=None,
            test_duration=None,
        )
        tv = NoIntersectionValidator(SimpleTestValidator())
        expected = False
        actual = tv.validate(test)
        assert actual == expected

    def test_no_sharp_turns_decorator_on_invalid_test(self):
        test = Test(
            0,
            road_points=[[10, 10], [100, 10], [145, 10], [148, 10], [150, 10], [150, 11], [150, 12], [150, 13]],
            test_outcome=None,
            test_duration=None,
        )
        tv = NoTooSharpTurnsValidator(SimpleTestValidator())
        expected = False
        actual = tv.validate(test)
        assert actual == expected

    def test_no_sharp_turns_decorator_on_valid_test(self):
        test = Test(
            0, road_points=[[10, 10], [100, 10], [145, 10], [148, 10], [150, 10]], test_outcome=None, test_duration=None
        )
        tv = NoTooSharpTurnsValidator(SimpleTestValidator())
        expected = True
        actual = tv.validate(test)
        assert actual == expected
