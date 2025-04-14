# tests/test_calculator.py

import pytest
from app.calculator import Calculator

@pytest.fixture
def calc():
    return Calculator()

def test_add(calc):
    assert calc.add(1, 2) == 3
    assert calc.add(-1, -1) == -2
    assert calc.add(0, 0) == 0
    assert calc.add(1.5, 2.5) == 4.0

def test_subtract(calc):
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 3) == -3
    assert calc.subtract(-2, -2) == 0
    assert calc.subtract(10, 0) == 10

def test_multiply(calc):
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(-2, 3) == -6
    assert calc.multiply(0, 10) == 0
    assert calc.multiply(1.5, 2) == 3.0

def test_divide(calc):
    assert calc.divide(10, 2) == 5
    assert calc.divide(-9, 3) == -3
    assert calc.divide(5.0, 2.0) == 2.5

def test_divide_by_zero(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)
