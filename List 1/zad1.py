from argparse import ArgumentParser
from random import randint
from enum import Enum
import typing


class DubstepStyle(Enum):
    CHILL_STEP = 1
    DROP_STEP = 2
    DARK_STEP = 3


def drop_sound(style: DubstepStyle) -> typing.Optional(str):
    if style == DubstepStyle.CHILL_STEP:
        return "Woooooob wuuuuuuub waaa"
    if style == DubstepStyle.DROP_STEP:
        return "Wobobobobobobbzzzz bzzzz krrr fff"
    if style == DubstepStyle.DARK_STEP:
        return "Noo ioo Ggooo aaaa"
    return None


def get_args():
    parser = ArgumentParser()
    parser.add_argument('n', type=int)
    return parser.parse_args()


def rounds():
    while True:
        yield randint(1, 2), randint(1, 2)


def print_scores(round_number: int, fr: int, sr: int, fs: int, ss: int) -> None:
    print("Round number: ", round_number, ".", sep="")
    print("First player rolls", fr, "and second player rolls", sr)
    print("Score is:", fs, "to", ss)


def match(rounds_number):
    first_score, second_score = 0, 0
    for r_num, (first_roll, second_roll) in enumerate(rounds()):
        if first_roll > second_roll:
            first_score += 1
        if second_roll > first_roll:
            second_score += 1
        print_scores(r_num, first_roll, second_roll, first_score, second_score)
        if rounds_number <= r_num and not first_score == second_score:
            break


if __name__ == "__main__":
    match(rounds_number=get_args().n)
