import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from math import pi
from mypackage.calculator import add, subtract, multiply, divide, sine, cosine, tangent


def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 5) == 5

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_sine():
    # Test sine of 90° if in radians, sine(pi/2) should be ~1
    assert sine(pi/2) == pytest.approx(1, rel=1e-2)

def test_cosine():
    # For cosine of 0, cosine(0) should be 1
    assert cosine(0) == pytest.approx(1, rel=1e-2)

def test_tangent():
    # Tangent of pi/4 should be ~1
    assert tangent(pi/4) == pytest.approx(1, rel=1e-2)

if __name__ == "__main__":
    pytest.main()