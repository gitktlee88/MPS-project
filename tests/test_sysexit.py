# content of test_sysexit.py
import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()

# content of test_class.py


class TestClass(object):
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello check"
        # assert hasattr(x, 'check')

# pytest.mark.parametrize decorator
# enables parametrization of arguments for a test function.

# content of test_expectation.py


@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 54),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected


# This will run the test with the arguments set to x=0/y=2, x=0/y=3, x=1/y=2 and x=1/y=3.
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    pass

# The ‘tmpdir’ fixture
# @pytest.fixture
# content of test_tmpdir.py


def test_create_file(tmpdir):
    print(tmpdir)
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
    # assert 0
