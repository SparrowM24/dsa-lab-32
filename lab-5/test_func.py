import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides


class TestGetTriangleType(unittest.TestCase):

    # + тесты

    def test_equilateral(self):
        self.assertEqual(get_triangle_type(5, 5, 5), "equilateral")
        self.assertEqual(get_triangle_type(0.1, 0.1, 0.1), "equilateral")

    def test_isosceles(self):
        self.assertEqual(get_triangle_type(6, 6, 7), "isosceles")
        self.assertEqual(get_triangle_type(5.5, 5.5, 6.0), "isosceles")

    def test_nonequilateral(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")
        self.assertEqual(get_triangle_type(2.5, 3.5, 4.5), "nonequilateral")

    # - тесты

    def test_negative_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-3, 4, 5)

    def test_zero_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 5, 5)

    def test_triangle_inequality(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, 3)

    def test_non_numeric(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type("5", 4, 5)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(5, None, 5)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(5, 4, [3])


if __name__ == '__main__':
    unittest.main(verbosity=2)