
import pytest

from src.calculator import add, divide,multiply

def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-2, -3) == -5

def test_divide():
    assert divide(10, 2) == 5

def test_multiply():
    assert multiply(10, 2) == 20

def test_divide_by_zero():
    with pytest.raises(ValueError) :
        divide(10, 0)
