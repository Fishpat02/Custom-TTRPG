from dataclasses import dataclass

import pandas as pd

from .dice import DieAdvantage, sum_prob_max, sum_prob_min


@dataclass
class Trial:
    dc: int
    proficient: bool
    advantage: DieAdvantage


def main() -> None:
    dcs = [10, 15, 20, 25]
    levels = [1, 5, 10, 15]
    roll_types = [
        "Flat",
        "Advantage",
        "Disadvantage",
        "Proficient",
        "Prof + Adv",
        "Prof + Dis",
    ]

    trials_data = []

    for dc in dcs:
        for l, level in enumerate(levels):
            prof_cap = l + 1

            trials = zip(
                roll_types,
                [
                    Trial(dc, False, DieAdvantage.NEUTRAL),
                    Trial(dc, False, DieAdvantage.ADVANTAGE),
                    Trial(dc, False, DieAdvantage.DISADVANTAGE),
                    Trial(dc, True, DieAdvantage.NEUTRAL),
                    Trial(dc, True, DieAdvantage.ADVANTAGE),
                    Trial(dc, True, DieAdvantage.DISADVANTAGE),
                ],
            )

            for name, trial in trials:
                trial_dice = 1
                if trial.proficient:
                    trial_dice += prof_cap

                if trial.advantage == DieAdvantage.ADVANTAGE:
                    trial_dice += 1

                if trial.advantage == DieAdvantage.DISADVANTAGE:
                    trial_dice -= 1 if trial_dice > 1 else 0

                probability = sum_prob_min(trial.dc, trial_dice)
                crit_probability = sum_prob_min(trial.dc + 10, trial_dice) or 0.0
                fail_probability = (
                    sum_prob_max(trial.dc - 10, trial_dice) or 1.0
                    if dc - 10 > 0 and trial_dice < dc - 10
                    else 0.0
                )

                trials_data += [
                    [trial_dice, probability, crit_probability, fail_probability]
                ]

    trials_frame = pd.DataFrame(
        index=pd.MultiIndex.from_product(
            [dcs, levels, roll_types],
            names=["dc", "level", "roll_type"],
        ),
        columns=["dice", "probability", "crit_probability", "fail_probability"],
        data=trials_data,
    )

    for dc, df in trials_frame.groupby("dc"):
        print(df)


if __name__ == "__main__":
    main()
