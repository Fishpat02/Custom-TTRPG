from functools import reduce
from operator import countOf

from .dice import DiceRoller, DieType


def main() -> None:
    REP_COUNT = 100
    DICE_PER_REP = 2
    ROLL_ADV = 1
    ROLL_DIS = 0

    low_rolls = mid_rolls = high_rolls = 0
    total_rolls = REP_COUNT * (DICE_PER_REP + ROLL_ADV - ROLL_DIS)

    for _ in range(REP_COUNT):
        roll = DiceRoller.roll_dice(
            DICE_PER_REP, advantage=bool(ROLL_ADV), disadvantage=bool(ROLL_DIS)
        )
        a, b = zip(*roll)
        diceValues: list[int] = list(a)
        diceTypes: list[DieType] = list(b)

        _value = reduce(lambda a, b: a + b, diceValues)

        low_rolls += countOf(diceTypes, DieType.BANE)
        mid_rolls += countOf(diceTypes, DieType.NEUTRAL)
        high_rolls += countOf(diceTypes, DieType.BOON)

    print()
    print(f"Low rolls %: {round((low_rolls / total_rolls) * 100, 1)}%")
    print(f"Mid rolls %: {round((mid_rolls / total_rolls) * 100, 1)}%")
    print(f"High rolls %: {round((high_rolls / total_rolls) * 100, 1)}%")
