# coding: utf8
import abc
from typing import Dict, Set
from Formula_exceptions import VariableNotAttributed
from itertools import product


class Formula(abc.ABC):
    @abc.abstractmethod
    def calculate(self, variables: Dict[str, bool]) -> bool:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def priority(self) -> int:
        pass

    @abc.abstractmethod
    def variables_contained(self) -> Set[str]:
        pass

    def is_tautology(self) -> bool:
        contained_variables = self.variables_contained()
        possible_dicts = list(dict(zip(contained_variables, evaluation))
                              for evaluation in product((True, False), repeat=len(contained_variables)))
        result = all(self.calculate(possible_dict) for possible_dict in possible_dicts)

        return result


class BinaryOperator(Formula):
    @property
    @abc.abstractmethod
    def linking_symbol(self) -> str:
        pass

    def __init__(self, f: Formula, s: Formula):
        self.f = f
        self.s = s

    def __str__(self):
        first_part = str(self.f) if self.f.priority > self.priority else "(" + str(self.f) + ")"
        second_part = str(self.s) if self.s.priority > self.priority else "(" + str(self.s) + ")"
        return first_part + self.linking_symbol + second_part

    def variables_contained(self) -> Set[str]:
        return self.f.variables_contained().union(self.s.variables_contained())


class And(BinaryOperator):
    priority = 10
    linking_symbol = " ^ "

    def calculate(self, variables: Dict[str, bool]) -> bool:
        f_val = self.f.calculate(variables)
        s_val = self.s.calculate(variables)
        return f_val and s_val


class Or(BinaryOperator):
    priority = 10
    linking_symbol = " v "

    def calculate(self, variables: Dict[str, bool]) -> bool:
        f_val = self.f.calculate(variables)
        s_val = self.s.calculate(variables)
        return f_val or s_val


class Implies(BinaryOperator):
    priority = 5
    linking_symbol = " => "

    def calculate(self, variables: Dict[str, bool]) -> bool:
        f_val = self.f.calculate(variables)
        s_val = self.s.calculate(variables)
        return (not f_val) or s_val


class IfAndOnlyIf(BinaryOperator):
    priority = 5
    linking_symbol = " <=> "

    def calculate(self, variables: Dict[str, bool]) -> bool:
        return self.f.calculate(variables) == self.s.calculate(variables)


class Not(Formula):
    priority = 15

    def __init__(self, negated: Formula):
        self.negated = negated

    def calculate(self, variables: Dict[str, bool]) -> bool:
        return not self.negated.calculate(variables)

    def __str__(self) -> str:
        return "~" + (str(self.negated) if self.negated.priority > self.priority else "(" + str(self.negated) + ")")

    def variables_contained(self) -> Set[str]:
        return self.negated.variables_contained()


class Constant(Formula):
    priority = 20

    def __init__(self, val: bool):
        self.val = val

    def calculate(self, variables: Dict[str, bool]) -> bool:
        return self.val

    def __str__(self) -> str:
        return "1" if self.val else "0"

    def variables_contained(self) -> Set[str]:
        return set()


class Variable(Formula):
    priority = 20

    def __init__(self, name: str):
        self.name = name

    def calculate(self, variables: Dict[str, bool]) -> bool:
        try:
            return variables[self.name]
        except KeyError:
            raise VariableNotAttributed(self.name)

    def __str__(self) -> str:
        return self.name

    def variables_contained(self) -> Set[str]:
        return {self.name}
