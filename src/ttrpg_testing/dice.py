from dataclasses import dataclass, field
from enum import Flag, auto
from functools import reduce
from random import randint

BANE_THRESHOLD: int = 3
BOON_THRESHOLD: int = 7

BASE_DICE_SIDES = 10


def n_combinations(target: int, dice: int, sides: int) -> int:
    combinations: int = 0

    if (dice * sides) < target:
        return combinations
    elif dice == 2:
        for s in range(sides):
            side = s + 1
            remaining = target - side

            if remaining <= 0:
                break

            if remaining <= sides:
                combinations += 1
    elif dice > 2:
        for s in range(sides):
            side = s + 1
            remaining = target - side

            if remaining < dice - 1:
                break

            combinations += n_combinations(remaining, dice - 1, sides)

    return combinations


def sum_prob(target: int, dice: int, sides: int = BASE_DICE_SIDES) -> float:
    probability_sum: float = 0.0

    for t in range(target, (dice * sides) + 1):
        probability_sum += n_combinations(t, dice, sides) / float(sides) ** dice

    return probability_sum


class DieType(Flag):
    BANE = auto()
    NEUTRAL = auto()
    BOON = auto()


@dataclass
class Die:
    value: int
    die_type: DieType


@dataclass
class Roll:
    dice: list[Die]
    value: int = field(init=False)

    def __post_init__(self):
        self.value = reduce(lambda a, b: a + b, [x.value for x in self.dice])


class DiceRoller:
    @staticmethod
    def roll_dice(
        count: int = 1, advantage: bool = False, disadvantage: bool = False
    ) -> Roll:
        rolls: list[Die] = []
        num_dice: int = count

        if advantage and disadvantage:
            raise ValueError("Cannot roll with both advantage AND disadvantage")

        if advantage:
            num_dice += 1
        elif disadvantage:
            num_dice -= 1 if num_dice > 1 else 0

        for _ in range(num_dice):
            roll: int = randint(1, 10)
            if roll <= BANE_THRESHOLD:
                rolls.append(Die(roll, DieType.BANE))
            elif roll <= BOON_THRESHOLD:
                rolls.append(Die(roll, DieType.NEUTRAL))
            else:
                rolls.append(Die(roll, DieType.BOON))

        return Roll(rolls)
