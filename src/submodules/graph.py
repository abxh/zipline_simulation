import matplotlib.pyplot as plt
from pandas import DataFrame


def three_axes(df: DataFrame):
    plt.rcParams["figure.autolayout"] = True  # better layout
    fig, ax = plt.subplots(ncols=3, figsize=(9, 6), dpi=100)
    df.plot(kind="scatter", x="t", y="R", ax=ax[0], color="tab:green")
    df.plot(kind="scatter", x="t", y="Rd", ax=ax[1], color="tab:green")
    df.plot(kind="scatter", x="t", y="Rdd", ax=ax[2], color="tab:green")
    plt.show()


def six_axes(df: DataFrame):
    plt.rcParams["figure.autolayout"] = True  # better layout
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(9, 12), dpi=100)
    df.plot(kind="scatter", x="t", y="R", ax=ax[0, 0], color="tab:green")
    df.plot(kind="scatter", x="t", y="Rd", ax=ax[0, 1], color="tab:green")
    df.plot(kind="scatter", x="t", y="Rdd", ax=ax[0, 2], color="tab:green")
    df.plot(kind="scatter", x="t", y="th", ax=ax[1, 0], color="tab:blue")
    df.plot(kind="scatter", x="t", y="thd", ax=ax[1, 1], color="tab:blue")
    df.plot(kind="scatter", x="t", y="thdd", ax=ax[1, 2], color="tab:blue")
    plt.show()
