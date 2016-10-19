# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

__author__ = 'kevin'


def test1():
    path = "/home/kevin/temp"
    xData = np.arange(0, 10, 1)
    yData1 = xData.__pow__(2.0)
    yData2 = np.arange(15, 61, 5)
    plt.figure(num=1, figsize=(8, 6))
    plt.title('Plot 1', size=14)
    plt.xlabel('x-axis', size=14)
    plt.ylabel('y-axis', size=14)
    plt.plot(xData, yData1, color='b', linestyle='--', marker='o', label='y1 data')
    plt.plot(xData, yData2, color='r', linestyle='-', label='y2 data')
    plt.legend(loc='upper left')
    plt.savefig(path + '/images/plot1.png', format='png')
    plt.show()

    mu = 0.0
    sigma = 2.0
    samples = np.random.normal(loc=mu, scale=sigma, size=1000)
    plt.figure(num=1, figsize=(8, 6))
    plt.title('Plot 2', size=14)
    plt.xlabel('value', size=14)
    plt.ylabel('counts', size=14)
    plt.hist(samples, bins=40, range=(-10, 10))
    plt.text(-9, 100, r'$\mu$ = 0.0, $\sigma$ = 2.0', size=16)
    #plt.savefig(path + '/images/plot2.png', format='png')
    plt.show()

    data = [33, 25, 20, 12, 10]
    plt.figure(num=1, figsize=(6, 6))
    plt.axes(aspect=1)
    plt.title('Plot 3', size=14)
    plt.pie(data, labels=('Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5'))
    #plt.savefig(path + '/images/plot3.png', format='png')
    plt.show()


def test_prepare_data():
    file_path = "/home/kevin/temp/data.txt"
    # 生成数据:row=4,column=6
    dataOut = np.arange(24).reshape(4, 6)
    print(dataOut)
    # 保存数据
    np.savetxt(file_path, dataOut, fmt='%.1f')
    # 读取数据
    data = np.loadtxt(file_path)
    print(data)


def test_plot():
    #mpl.rcParams['font.family'] = 'sans-serif'
    #mpl.rcParams['font.sans-serif'] = [u'SimHei']

    data = np.random.randint(1, 11, 5)
    print data
    x = np.arange(len(data))

    plt.plot(x, data, color = 'r')
    plt.show()
    plt.bar(x, data, alpha = .5, color = 'g')
    plt.show()
    plt.pie(data, explode = [0,0,.2, 0, 0])
    plt.show()


def test_plot2():
    data = np.random.randint(1, 5, (5, 2))
    print data
    x = np.arange(len(data))

    plt.plot(x, data[:, 0], '--', color = 'm')
    plt.plot(x, data[:, 1], '-.', color = 'b')

    plt.show()

if __name__ == '__main__':
    #test1()

    #test_prepare_data()
    test_plot()
    #test_plot2()

    pass
