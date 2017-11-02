from unittest import TestCase
from parameterized import parameterized
from List3.zad2 import perfect_comprehension, perfect_functional, perfect_iterator


class TestData:
    @staticmethod
    def perfect_data():
        yield 1, []

        yield 4, []

        yield 6, [6]

        yield 700, [6, 28, 496]


class TestPerfectFunctional(TestCase):
    @parameterized.expand(TestData.perfect_data())
    def test_perfect_functional(self, arg, ans):
        self.assertEqual(perfect_functional(arg), ans)


class TestPerfectComprehension(TestCase):
    @parameterized.expand(TestData.perfect_data())
    def test_perfect_comprehension(self, arg, ans):
        self.assertEqual(perfect_comprehension(arg), ans)


class TestPerfectIterator(TestCase):
    @parameterized.expand(TestData.perfect_data())
    def test_perfect_iterator(self, arg, ans):
        self.assertEqual(list(perfect_iterator(arg)), ans)
