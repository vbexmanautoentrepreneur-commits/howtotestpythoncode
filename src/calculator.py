def add(a, b):
    return a + b

def divide(a, b):
    if b==0:
        raise ValueError("division par zero not possible")
    return a / b

def multiply(a, b):
    return a * b
