from dataclasses import dataclass

from .dice import DieAdvantage, sum_prob


@dataclass
class Trial:
    dc: int
    proficient: bool
    advantage: DieAdvantage


def main() -> None:
    num_trials: int = 20

    for i, v in enumerate(range(1, num_trials, 4)):
        level = v
        num_dice = 1 + i

        trial = Trial(15, True, DieAdvantage.NEUTRAL)

        if trial.proficient:
            num_dice += 1

        if trial.advantage & DieAdvantage.ADVANTAGE:
            num_dice += 1
        elif trial.advantage & DieAdvantage.DISADVANTAGE:
            num_dice -= 1 if num_dice > 1 else 0

        probability = sum_prob(15, num_dice)

        print(
            f"Probability to pass DC 15 at level {level} rolling {num_dice} dice: {probability:.2%}"
        )
