# -*- coding:utf-8 -*-

from __future__ import print_function

import os

from operator import add
from pyspark import SparkContext, SparkConf

__author__ = 'kevin'


def my_print(l):
    # 中文测试
    print(l)

if __name__ == '__main__':
    master = "local[1]"
    app_name = "spark_sql_wc"
    input = 'hdfs://debian:8020/input/words.csv'

    spark_home = '/home/kevin/galaxy/spark-1.6.2-bin-hadoop2.6'
    os.environ['SPARK_HOME'] = spark_home

    conf = (SparkConf()
            .setMaster(master)
            .setAppName(app_name))
            #.set("spark.executor.extraClassPath",'mysql-connector-java-5.1.18.jar')
            #.set('spark.io.compression.codec','snappy'))
    sc = SparkContext(conf=conf)

    #sum = sc.accumulator(0)
    #bcv = sc.broadcast([1,2,3])

    lines = sc.textFile(input)

    word_count = lines.flatMap(lambda line: line.split(","))\
        .map(lambda word: (word, 1))\
        .reduceByKey(add)
    word_count.foreach(my_print)


    #print bcv.value
    sc.stop()


