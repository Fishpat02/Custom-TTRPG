from . import gen_dataframe


def main() -> None:
    trials_frame = gen_dataframe()

    for dc, df in trials_frame.group_by("dc", maintain_order=True):
        print(df)


if __name__ == "__main__":
    main()
