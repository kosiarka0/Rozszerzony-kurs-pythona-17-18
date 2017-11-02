from timeit import timeit
from contextlib import redirect_stdout
from random import sample, seed
from tqdm import tqdm

if __name__ == "__main__":

    with open("zad3_results.txt", "w") as f:
        with redirect_stdout(f):
            for limit_in in tqdm(sorted(sample(range(2, 1000), 10))):
                print("Functional", limit_in, ":", timeit(setup="from List3.zad3 import fractional_functional",
                                                          stmt="fractional_functional(" + str(limit_in) + ")",
                                                          number=1000))
                print("Comprehension", limit_in, ":", timeit(setup="from List3.zad3 import fractional_comprehension",
                                                             stmt="fractional_comprehension(" + str(limit_in) + ")",
                                                             number=1000))
                print("My", limit_in, ":", timeit(setup="from List3.zad3 import my_fractional",
                                                  stmt="my_fractional(" + str(limit_in) + ")",
                                                  number=1000))
                print("-" * 15)
