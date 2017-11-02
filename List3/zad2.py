import typing


def perfect_functional(n: int) -> typing.List[int]:
    return list(
        filter(
            lambda x: sum(filter(lambda y: x % y == 0, range(1, x // 2 + 1))) == x,
            range(1, n + 1)))


def perfect_comprehension(n: int) -> typing.List[int]:
    return [x for x in range(1, n + 1) if sum(y for y in range(1, x // 2 + 1) if not x % y) == x]


def perfect_iterator(n: int):
    for num in range(1, n + 1):
        if sum(elem for elem in range(1, num // 2 + 1) if num % elem == 0) == num:
            yield num
