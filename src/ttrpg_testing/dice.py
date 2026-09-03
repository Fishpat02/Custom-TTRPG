from enum import Flag, auto
from random import randint

BANE_THRESHOLD: int = 3
BOON_THRESHOLD: int = 7


class DieType(Flag):
    BANE = auto()
    NEUTRAL = auto()
    BOON = auto()


class DiceRoller:
    @staticmethod
    def roll_dice(
        count: int = 1, advantage: bool = False, disadvantage: bool = False
    ) -> list[tuple[int, DieType]]:
        rolls: list[tuple[int, DieType]] = []
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
                rolls.append((roll, DieType.BANE))
            elif roll <= BOON_THRESHOLD:
                rolls.append((roll, DieType.NEUTRAL))
            else:
                rolls.append((roll, DieType.BOON))

        return rolls
