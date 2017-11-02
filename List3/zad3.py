from itertools import count, takewhile, groupby
from functools import reduce
import typing


def primes(n):
    primes_list = []
    nums_list = [None for _ in range(n)]  # type: typing.List[typing.Optional[int]]
    for num in range(2, n):
        if nums_list[num] is None:
            yield num
            primes_list.append(num)
            nums_list[num] = len(primes_list)
        for idx, prime in enumerate(primes_list[:(nums_list[num] + 1)]):
            if num * prime >= n:
                break
            nums_list[num * prime] = idx


def fractional_functional(n: int) -> typing.List[typing.Tuple[int, int]]:
    def my_f(act, dividor):
        act_num, act_l = act
        div_times = sum(1 for _ in takewhile(lambda x: n % dividor ** x == 0, count(1)))
        return act_num // dividor ** div_times, act_l + [(dividor, div_times)]

    return reduce(my_f, filter(lambda p: n % p == 0, primes(n + 1)), (n, []))[1]


def fractional_comprehension(n: int) -> typing.List[typing.Tuple[int, int]]:
    return [(dividor, len([None for x in range(1, n // dividor + 1) if n % dividor ** x == 0])) for
            dividor in primes(n + 1) if n % dividor == 0]


def fractional_iterator(arg):
    for prime in primes(arg + 1):
        if arg % prime == 0:
            div_times = sum(1 for _ in takewhile(lambda x: arg % prime ** x == 0, count(1)))
            yield prime, div_times
            arg //= prime ** div_times
            continue
        if arg == 1:
            return


if __name__ == "__main__":
    print(list(primes(31)))
