from app import calc


def test_add():
    assert calc.add(3, 5) == 8
    assert calc.add(6, 4) == 10


def test_multiply():
    assert calc.multiply(5, 5) == 25
    assert calc.multiply(6, 2) == 12

def test_subtract():
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(7, 1) == 6

def test_divide():
    assert calc.divide(10, 2) == 5
    assert calc.divide(6, 2) == 3
    
def test_square():
    assert calc.square(3) == 9
    assert calc.square(4) == 16

def test_cube():
    assert calc.cube(2) == 8
    assert calc.cube(3) == 27