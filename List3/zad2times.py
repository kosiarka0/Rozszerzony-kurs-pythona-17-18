from timeit import timeit
from contextlib import redirect_stdout
from random import sample
from tqdm import tqdm

if __name__ == "__main__":
    with open("zad2_results.txt", "w") as f:
        with redirect_stdout(f):
            for limit_in in tqdm(sorted(sample(range(2, 1000), 10))):
                print("Functional", limit_in, ":", timeit(setup="from List3.zad2 import perfect_functional",
                                                          stmt="perfect_functional(" + str(limit_in) + ")",
                                                          number=1000))
                print("Comprehension", limit_in, ":", timeit(setup="from List3.zad2 import perfect_comprehension",
                                                             stmt="perfect_comprehension(" + str(limit_in) + ")",
                                                             number=1000))
                print("-" * 15)
