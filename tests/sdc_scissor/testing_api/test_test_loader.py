import pathlib

import pytest

from sdc_scissor.testing_api.test_loader import TestLoader


class TestTestLoader:
    def test_empty_test_folder_should_have_no_next_test(self, mocker):
        empty_test_dir_mock = mocker.patch("pathlib.Path")
        test_loader = TestLoader(tests_dir=empty_test_dir_mock)
        has_next = test_loader.has_next()
        assert not has_next

    def test_empty_test_folder_should_have_no_next_test_and_throw_exception_on_next(self, mocker):
        empty_test_dir_mock = mocker.patch("pathlib.Path")
        test_loader = TestLoader(tests_dir=empty_test_dir_mock)
        with pytest.raises(Exception):
            _ = test_loader.next()

    def test_non_empty_test_folder_should_have_next_test(self, mocker, fs):
        fs.makedir(r"./tests")
        fs.makedir(r"./tests/unlabeled")
        fs.create_file(r"./tests/test.json")
        fs.create_file(r"./tests/no-match.json")
        fs.create_file(r"./tests/unlabeled/test.json")
        non_empty_test_dir_mock = pathlib.Path("./tests")
        test_loader = TestLoader(tests_dir=non_empty_test_dir_mock)
        test_loader.test_paths = [mocker.stub(), mocker.stub()]
        has_next = test_loader.has_next()
        assert has_next
