# -*- coding:utf-8 -*-
import pandas as pd

__author__ = 'kevin'


class PandasUtils:
    def __init__(self):
        pass

    @staticmethod
    def encoding(feature, encode_dict):
        # replace value
        encode_feature = pd.Series(feature, copy=True)
        for key, value in encode_dict.items():
            encode_feature.replace(key, value, inplace=True)
        return encode_feature

    @staticmethod
    def binning(feature, bins, labels=None):
        # 连续型数字
        min_val = feature.min()
        max_val = feature.max()
        cut_points = [min_val] + bins + [max_val]
        print cut_points
        # 如果没有标签，则使用默认标签0 ... (n-1)
        if not labels:
            labels = range(len(bins) + 1)
        bin_feature = pd.cut(feature, bins=cut_points, labels=labels, include_lowest=True)
        return bin_feature

