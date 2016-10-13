__author__ = 'kevin'

import numpy as np


def mean():
    l = [[1, 2, 3, 4, 5, 6], [10, 2, 3, 4, 5, 60]]
    avg_column = np.mean(l, axis=0)
    print(avg_column)
    avg_row = np.mean(l, axis=1)
    print(avg_row)


def file():
    path = "/home/kevin/users.csv"
    file = open(path, "r")
    matrix = np.loadtxt(file, delimiter=",", skiprows=0)
    avg_column = np.mean(matrix, axis=0)

    print(avg_column)

    for avg in avg_column:
        print(avg)


if __name__ == '__main__':
    # mean()
    file()

    pass
