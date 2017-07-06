# -*- coding: utf-8 -*-

import os as os
import pandas as pd
import my_functions_for_diplom as my


def func(x):

    if x.first_valid_index() is None:
        return None
    else:
        return x.first_valid_index()

files = list()
matsum = 0
samples = my.decode()

keyword = "mass"

for file in os.listdir('data'):
    if file.startswith(keyword):
        files.append(file)

files.sort()
result = pd.DataFrame(index = ['Yx','Ycr'])

for file in files:

    df_d = pd.DataFrame()
    df_G = pd.DataFrame()
    df_K = pd.DataFrame()
    df_K1 = pd.DataFrame()

    df = pd.read_csv(my.dir_data+file, sep='\t', header=0, encoding="utf-8")
    del df['m']

    for name in list(df):
        if name == 'k':
            df_d[name] = df[name].diff()
            df_G[name] = df_d[name]/(1.5*60)
        else:
            df_d[name] = df[name].dropna().diff()
            df_G[name] = df_d[name].dropna()/(1.5*60)

    df_sum = df_d.cumsum()
    df_G = df_G.cumsum()

    first_non_nan = df_sum.apply(func)  # find index of first num (nonNaN)
    
    for name in list(df_sum):
        i = first_non_nan[name]-1
        df_sum[name][i] = 0

    df_G = df_G[df_G.k != 0].dropna(subset=['k'])

    num = 1
    for s in file:
        try:
            num = int(s)
        except ValueError:
            pass

    # CALC EFF
    for name in list(df_G):
        if name != 'k':
            df_K[name] = - df_G[name] / df_G['k']
            df_K1 = pd.concat([df_K1, df_K[name].dropna()])

    df_K1 = df_K1.sort_index()
    df_K1 = df_K1[df_K1 > 0]

    starttime = int(df_K1.apply(func))
    xtime = df_sum['k'].iloc[starttime:].idxmax() #
    crtime = df_sum['k'].iloc[starttime:]
    crtime = crtime[crtime < 0].idxmax()

    Kx = df_K1.iloc[:xtime].mean()[0]
    Kcr = df_K1.iloc[:crtime].mean()[0]

    if starttime == 1:
        Yx = Kx * xtime * df_sum['k'][xtime]
        Ycr = Kcr * crtime * df_sum['k'][crtime-1]
    else:
        Yx = Kx * (xtime+1-starttime) * df_d['k'].iloc[starttime:(xtime+1)].sum()
        Ycr = Kcr * (crtime-starttime) * df_d['k'][starttime:(crtime - 1)].sum()

    colname = samples[num]
    df_sum.to_csv(my.dir_output+"gravi_cumsum_"+colname+".csv", index=False, sep='\t', encoding='utf-8')
    result[colname] = [Yx*1000, Ycr*1000]
result.to_csv(my.dir_output+"gravi_eff.csv", index=True, sep='\t', encoding='utf-8')
print(result)
