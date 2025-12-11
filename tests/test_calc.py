from app import calc


def test_add():
    assert calc.add(2, 3) == 5
    assert calc.add(6, 3) == 9


def test_multiply():
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(6, 2) == 12

def test_subtract():
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(7, 1) == 6

def test_divide():
    assert calc.divide(10, 2) == 5
    assert calc.divide(6, 2) == 3
    
