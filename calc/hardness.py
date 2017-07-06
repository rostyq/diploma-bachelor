# -*- coding: utf-8 -*-

import pandas as pd
import my_functions_for_diplom as my

samples = my.decode()

df = pd.read_csv(my.dir_data+'hardness.csv', sep='\t', header=0, encoding="utf-8")

df = my.rename_col(df, samples)
df = df.fillna(2.4)  # average microhardness of steel_45

# taking max
df_max = pd.DataFrame(df.ix[:, df.columns != 'depth'].max(), columns=['max_hard'])
df_max = df_max.round(1)

df_max.to_csv(my.dir_output+"hard_comparison.csv", index=True, index_label='sample', sep='\t', encoding='utf-8')
df.to_csv(my.dir_output+"hard.csv", index=False, sep='\t', encoding='utf-8')
