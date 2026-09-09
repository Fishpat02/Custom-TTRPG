from dataclasses import dataclass

from .dice import DieAdvantage, sum_prob_max, sum_prob_min


@dataclass
class Trial:
    dc: int
    proficient: bool
    advantage: DieAdvantage


def main() -> None:
    for _, dc in enumerate([10, 15, 20, 25]):
        for prof_cap, level in enumerate([1, 5, 10, 15]):
            num_dice = 1

            trials = [
                ("Flat", Trial(dc, False, DieAdvantage.NEUTRAL)),
                ("Advantage", Trial(dc, False, DieAdvantage.ADVANTAGE)),
                ("Disadvantage", Trial(dc, False, DieAdvantage.DISADVANTAGE)),
                ("Proficient", Trial(dc, True, DieAdvantage.NEUTRAL)),
                ("Prof + Adv", Trial(dc, True, DieAdvantage.ADVANTAGE)),
                ("Prof + Dis", Trial(dc, True, DieAdvantage.DISADVANTAGE)),
            ]

            print(f"Probability to pass DC {dc} roll at level {level}:")

            for trial in trials:
                trial_dice = num_dice
                if trial[1].proficient:
                    trial_dice += 1 + prof_cap

                if trial[1].advantage == DieAdvantage.ADVANTAGE:
                    trial_dice += 1

                if trial[1].advantage == DieAdvantage.DISADVANTAGE:
                    trial_dice -= 1 if trial_dice > 1 else 0

                probability = sum_prob_min(trial[1].dc, trial_dice)
                crit_probability = sum_prob_min(trial[1].dc + 10, trial_dice) or 0.0
                fail_probability = (
                    sum_prob_max(trial[1].dc - 10, trial_dice) or 1.0
                    if dc - 10 > 0
                    else 0.0
                )

                print(
                    f"{trial[0]:>15}: {probability:7.2%} [{crit_probability:7.2%} Critical Success] [{fail_probability:7.2%} Critical Failure] ({trial_dice} dice)"
                )

            print()

        print(
            "------------------------------------------------------------------------------------------\n"
        )
