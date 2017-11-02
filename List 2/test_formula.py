from unittest import TestCase
from parameterized import parameterized
from Formula import *
from Formula_exceptions import VariableNotAttributed


class DataForTestFormula:
    @staticmethod
    def calculate_data():
        yield ("Basic true constant",
               Constant(True),
               None,
               True)

        yield ("Basic false constant",
               Constant(False),
               None,
               False)

        yield ("Single true variable",
               Variable("a"),
               {"a": True},
               True)

        yield ("Single false variable",
               Variable("b"),
               {"b": False},
               False)

        yield ("Basic And operator",
               And(Constant(True), Constant(False)),
               None,
               False)

        yield ("Basic Or operator",
               Or(Constant(True), Constant(False)),
               None,
               True)

        yield ("Basic Implies operator",
               Implies(Constant(False), Constant(True)),
               None,
               True)

        yield ("Basic IfAndOnlyIf operator",
               IfAndOnlyIf(Constant(False), Constant(False)),
               None,
               True)

    @staticmethod
    def calculate_raises_variable_not_attributed_data():
        yield ("Basic",
               Variable("x"),
               dict())

        yield ("Lazy Or 1",
               Or(Variable("x"), Constant(True)),
               dict())

        yield ("Lazy Or 2",
               Or(Constant(True), Variable("x")),
               dict())

        yield ("Lazy And 1",
               And(Variable("x"), Constant(False)),
               dict())

        yield ("Lazy And 2",
               And(Constant(False), Variable("x")),
               dict())

    @staticmethod
    def str_data():
        yield ("Basic variable",
               Variable("x"),
               "x")

        yield ("True constant",
               Constant(True),
               "1")

        yield ("False constant",
               Constant(False),
               "0")

        yield ("Basic And",
               And(Variable("x"), Variable("y")),
               "x ^ y")

        yield ("Basic Or",
               Or(Variable("a"), Variable("b")),
               "a v b")

        yield ("Basic Implies",
               Implies(Variable("a"), Constant(True)),
               "a => 1")

        yield ("Basic IfAndOnlyIf",
               IfAndOnlyIf(Constant(True), Constant(False)),
               "1 <=> 0")

        yield ("Double implication",
               Implies(
                   Implies(
                       Variable("x"),
                       Variable("y")
                   ),
                   Variable("z")
               ),
               "(x => y) => z"
               )

        yield ("And Implies Or",
               Implies(
                   And(
                       Variable("x"),
                       Variable("y")
                   ),
                   Or(Variable("z"),
                      Variable("q"))
               ),
               "x ^ y => z v q"
               )

    @staticmethod
    def is_tautology_data():
        yield ("Constant true",
               Constant(True),
               True)

        yield ("Constant false",
               Constant(False),
               False)

        yield ("Single variable",
               Variable("x"),
               False)

        yield ("Law of excluded middle",
               Or(Variable("x"), Not(Variable("x"))),
               True)

        yield ("X and not X",
               And(Variable("x"), Not(Variable("x"))),
               False)

        yield ("False implies everything",
               Implies(
                   And(
                       Variable("x"),
                       Not(Variable("x"))
                   ),
                   Variable("y")
               ),
               True)

        yield ("Reversed implication",
               IfAndOnlyIf(
                   Implies(
                       Variable("x"),
                       Variable("y")
                   ),
                   Implies(
                       Not(Variable("y")),
                       Not(Variable("x"))
                   )
               ),
               True)

        yield ("Few Or",
               Or(Variable("x"), Or(Variable("y"), Variable("z"))),
               False)


class TestFormula(TestCase):
    @parameterized.expand(DataForTestFormula.calculate_data())
    def test_calculate(self, _, formula, variables_dict, expected):
        self.assertEqual(formula.calculate(variables_dict), expected)

    @parameterized.expand(DataForTestFormula.calculate_raises_variable_not_attributed_data())
    def test_calculate_raises_VariableNotAttributed(self, _, formula, variables_dict):
        with self.assertRaises(VariableNotAttributed, ):
            formula.calculate(variables_dict)

    @parameterized.expand(DataForTestFormula.str_data())
    def test_str(self, _, formula, expected_str):
        self.assertEqual(str(formula), expected_str)

    @parameterized.expand(DataForTestFormula.is_tautology_data())
    def test_is_tautology(self, _, formula, expected_result):
        self.assertEqual(formula.is_tautology(), expected_result)
