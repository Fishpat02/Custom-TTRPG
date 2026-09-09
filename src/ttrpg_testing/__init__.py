from dataclasses import dataclass

from .dice import DieAdvantage, sum_prob


@dataclass
class Trial:
    dc: int
    proficient: bool
    advantage: DieAdvantage


def main() -> None:
    for i, v in enumerate([1, 5, 10, 15]):
        level = v
        num_dice = 1 + i

        trials = [
            ("Flat", Trial(15, False, DieAdvantage.NEUTRAL)),
            ("Advantage", Trial(15, False, DieAdvantage.ADVANTAGE)),
            ("Disadvantage", Trial(15, False, DieAdvantage.DISADVANTAGE)),
            ("Proficient", Trial(15, True, DieAdvantage.NEUTRAL)),
            ("Prof + Adv", Trial(15, True, DieAdvantage.ADVANTAGE)),
            ("Prof + Dis", Trial(15, True, DieAdvantage.DISADVANTAGE)),
        ]

        print(f"Probability to pass DC 15 roll at level {level}:")

        for trial in trials:
            trial_dice = num_dice
            if trial[1].proficient:
                trial_dice += 1

            if trial[1].advantage == DieAdvantage.ADVANTAGE:
                trial_dice += 1

            if trial[1].advantage == DieAdvantage.DISADVANTAGE:
                trial_dice -= 1 if trial_dice > 1 else 0

            probability = sum_prob(trial[1].dc, trial_dice)

            print(f"{trial[0]:>15}: {probability:.2%} ({trial_dice} dice)")

        print()
