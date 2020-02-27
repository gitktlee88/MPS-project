import pytest
from filefunc import File_Func


@pytest.fixture
def filename():
    filename = "tests_mytest/data.json"
    return filename


@pytest.fixture
def create_File_Func():
    file1 = File_Func()
    return file1


def test_file_exists(filename, create_File_Func):
    if create_File_Func.check_file_exists(filename):
        assert True
    else:
        assert False


def test_read_file(filename, create_File_Func):
    dataset = create_File_Func.read_file(filename)
    if dataset:
        assert True
    else:
        assert False
