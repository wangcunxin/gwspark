__author__ = 'kevin'

import numpy as np


def mean():
    l = [[1, 2, 3, 4, 5, 6], [10, 2, 3, 4, 5, 60]]
    avg_column = np.mean(l, axis=0)
    print(avg_column)
    avg_row = np.mean(l, axis=1)
    print(avg_row)


def file():
    path = "/home/kevin/temp/users.csv"
    file = open(path, "r")
    matrix = np.loadtxt(file, delimiter=",", skiprows=0)
    avg_column = np.mean(matrix, axis=0)
    file_avg = open("/home/kevin/temp/users-avg.csv","w")
    #print(avg_column)
    arr = []
    for i in range(0,len(avg_column)):
        #print(avg_column[i])
        avg = round(avg_column[i],2)
        arr.append("%d\t%s\n" % (i,avg))
        #arr.append(avg)

    print(arr)
    #np.savetxt('/home/kevin/temp/users-avg.csv', arr, delimiter=',')
    file_avg.writelines(arr)
    file.close()
    file_avg.close()

if __name__ == '__main__':
    # mean()
    file()

    pass
