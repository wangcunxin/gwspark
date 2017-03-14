# -*- coding:utf-8 -*-

from __future__ import print_function

import os

from operator import add
from pyspark import SparkContext, SparkConf

__author__ = 'kevin'


def filter_special(kv,words):
    #sum +=1
    ret = True
    if kv[0].strip() in words:
        ret = False
    return ret
if __name__ == '__main__':
    master = "local[1]"
    app_name = "spark_sql_wc"
    input = 'hdfs://alice:8020/user/hadoop/input/*'

    spark_home = '/home/kevin/galaxy/spark-2.1.0-bin-hadoop2.6'
    os.environ['SPARK_HOME'] = spark_home

    conf = (SparkConf()
            .setMaster(master)
            .setAppName(app_name))
            #.set("spark.executor.extraClassPath",'mysql-connector-java-5.1.18.jar')
            #.set('spark.io.compression.codec','snappy'))
    sc = SparkContext(conf=conf)

    sum = sc.accumulator(0,"my accumulator")
    bcv = sc.broadcast(["etc","and","models"])

    lines = sc.textFile(input)

    word_count = lines.flatMap(lambda line: line.split(","))\
        .map(lambda word: (word, 1))\
        .reduceByKey(add).filter(lambda kv:filter_special(kv,bcv.value))
    word_count.foreach(print)

    print(sum.value)

    sc.stop()


