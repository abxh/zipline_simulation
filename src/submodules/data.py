import os

import numpy as np
import pandas as pd


def euler(y0, h, f_val):
    return y0 + h * f_val


# https://stackoverflow.com/questions/13852700/create-file-but-if-name-exists-add-number
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "_" + str(counter) + extension
        counter += 1

    return path


class DataHolder:
    def __init__(self, total_time_s: float, samples: int):
        self.data = pd.DataFrame({"t": np.linspace(0, total_time_s, samples)})

        if not os.path.exists("data"):
            os.makedirs("data")

    def set_val(self, i, column, val):
        rowIndex = self.data.index[i]
        self.data.loc[rowIndex, column] = val

    def get_val(self, i, column):
        return self.data.at[i, column]

    def save(self):
        path = uniquify("data/test.xlsx")
        self.data.to_excel(path, index=False)
        return path

    @property
    def length(self):
        return self.data.shape[0]
