# -*- coding: utf-8 -*-


def decode(filename="data/sample_codes.txt"):
    """
    This func decode my specimens. It returns dictionary with entries like >>> 1:'sample_name'.
    :param filename:
    :return decode_dict:
    """
    decode_dict = {}
    with open(filename) as f:
        for line in f:
            (key, val) = line.split(',')
            decode_dict[int(key)] = val[:-1]
    return decode_dict


def rename_col(pandas_dataframe, decode_dict):
    """
   This func renames column names in pandas data frame according to strings in decode_dict.
   Use only for pandas.
    :param pandas_dataframe:
    :param decode_dict:
    :return pandas_dataframe:
   """
    for i in list(decode_dict.keys()):
        pandas_dataframe = pandas_dataframe.rename(columns={str(i): decode_dict[i]})
    return pandas_dataframe

dir_data = 'data/'
dir_output = 'output_data/'

#RENGEN
lamb = 1.54059  # лямбда випромінювання
delta = 0.015

k4 = [1, 2.66, 3.67, 5.33, 6.33, 8, 9, 10.67, 11.67, 13.33]
hkl_k4 = ['111','200','311']
k6 =[1, 2, 3, 4, 5, 6, 8, 9, 10, 11]
hkl_k6 = ['100', '110', '111', '200']#test
k8 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
hkl_k8 = ['100', '110', '111', '200']#test
k12 =[1, 1.33, 2.66, 3.37, 4, 5.33, 6.33, 6.67, 8, 9]
hkl_k12 = ['111', '200', '220', '311', '222']
k = [k4, k6, k8, k12]
hkl_k = [hkl_k4,hkl_k6,hkl_k8,hkl_k12]