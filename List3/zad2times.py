from timeit import timeit
import csv
from tqdm import tqdm


def prepare_data():
    for limit_in in tqdm( range(1,2000,50)):
        yield {"Function": "Functional", "Limit": limit_in,
               "Time": timeit(setup="from List3.zad2 import perfect_functional",
                              stmt="perfect_functional(" + str(limit_in) + ")", number=1000)}

        yield {"Function": "Comprehension", "Limit": limit_in,
               "Time": timeit(setup="from List3.zad2 import perfect_comprehension",
                              stmt="perfect_comprehension(" + str(limit_in) + ")", number=1000)}

        yield {"Function": "Iterable", "Limit": limit_in,
               "Time": timeit(setup="from List3.zad2 import perfect_iterator",
                              stmt="perfect_iterator({})".format(limit_in), number=1000)}


if __name__ == "__main__":
    with open("zad2_data.csv", "w") as f:
        dw = csv.DictWriter(f, ["Function", "Limit", "Time"])
        dw.writeheader()
        dw.writerows(prepare_data())
