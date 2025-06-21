import math

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    """Raise a to the power of b."""
    return a ** b

def root(a, n):
    """Calculate the nth root of a. Raises an error for invalid cases."""
    if n == 0:
        raise ValueError("Zeroth root is not defined")
    
    # Raise an error if 'a' is negative and 'n' is even,
    # since this would result in a complex number.
    if a < 0 and n % 2 == 0:
        raise ValueError("Cannot take an even root of a negative number")
    
    return a ** (1 / n)

def sine(angle):
    """Return the sine of the given angle (in radians)."""
    return math.sin(angle)

def cosine(angle):
    """Return the cosine of the given angle (in radians)."""
    return math.cos(angle)

def tangent(angle):
    """Return the tangent of the given angle (in radians)."""
    return math.tan(angle)