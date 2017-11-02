from timeit import timeit
import csv
from tqdm import tqdm


def prepare_data():
    for limit_in in tqdm( range(2,1000)):
        yield {"Function": "Functional", "Limit": limit_in,
               "Time": timeit(setup="from List3.zad3 import fractional_functional",
                              stmt="fractional_functional(" + str(limit_in) + ")", number=1000)}

        yield {"Function": "Comprehension", "Limit": limit_in,
               "Time": timeit(setup="from List3.zad3 import fractional_comprehension",
                              stmt="fractional_comprehension(" + str(limit_in) + ")", number=1000)}

        yield {"Function": "Iterable", "Limit": limit_in,
               "Time": timeit(setup="from List3.zad3 import fractional_iterator",
                              stmt="list(fractional_iterator({}))".format(limit_in), number=1000)}


if __name__ == "__main__":
    with open("zad3_more_data.csv", "w") as f:
        dw = csv.DictWriter(f, ["Function", "Limit", "Time"])
        dw.writeheader()
        dw.writerows(prepare_data())