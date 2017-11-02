from unittest import TestCase
from List3.zad3 import fractional_comprehension, fractional_functional, fractional_iterator
from parameterized import parameterized


class TestData:
    @staticmethod
    def fractional_data():
        yield 1, []

        yield 4, [(2, 2)]

        yield 6, [(2, 1), (3, 1)]

        yield 10, [(2, 1), (5, 1)]

        yield 13, [(13, 1)]

        yield 700, [(2, 2), (5, 2), (7, 1)]

        yield 325, [(5, 2), (13, 1)]


class TestFractionalFunctional(TestCase):
    @parameterized.expand(TestData.fractional_data())
    def test_fractional_functional(self, arg, ans):
        self.assertEqual(fractional_functional(arg), ans)


class TestFractionalComprehension(TestCase):
    @parameterized.expand(TestData.fractional_data())
    def test_fractional_comprehension(self, arg, ans):
        self.assertEqual(fractional_comprehension(arg), ans)


class TestMyFractional(TestCase):
    @parameterized.expand(TestData.fractional_data())
    def test_my_fractional(self, arg, ans):
        self.assertEqual(list(fractional_iterator(arg)), ans)
