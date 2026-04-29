import pytest
from triangle_class import Triangle
from triangle_func import IncorrectTriangleSides


@pytest.fixture
def equilateral():
    return Triangle(5, 5, 5)


@pytest.fixture
def isosceles():
    return Triangle(6, 6, 7)


@pytest.fixture
def nonequilateral():
    return Triangle(3, 4, 5)


# + Тесты

def test_triangle_creation_positive():
    t = Triangle(3, 4, 5)
    assert t.a == 3
    assert t.b == 4
    assert t.c == 5


def test_equilateral_type(equilateral):
    assert equilateral.triangle_type() == "equilateral"


def test_isosceles_type(isosceles):
    assert isosceles.triangle_type() == "isosceles"


def test_nonequilateral_type(nonequilateral):
    assert nonequilateral.triangle_type() == "nonequilateral"


def test_perimeter(equilateral, isosceles, nonequilateral):
    assert equilateral.perimeter() == 15
    assert isosceles.perimeter() == 19
    assert nonequilateral.perimeter() == 12


# - Тесты

def test_invalid_creation_negative():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 5, 5)

    with pytest.raises(IncorrectTriangleSides):
        Triangle(-3, 4, 5)

    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 2, 3)

    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 1, 100)

    with pytest.raises(IncorrectTriangleSides):
        Triangle("5", 4, 5)


if __name__ == "__main__":
    pytest.main(["-v", __file__])