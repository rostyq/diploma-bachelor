# -*- coding: utf-8 -*-

import pandas as pd
import my_functions_for_diplom as my

samples = my.decode()

df = pd.read_csv(my.dir_data + 'df_wear.csv', sep='\t', index_col='time', encoding="utf-8")
df_steel = pd.read_csv(my.dir_data + 'df_wear_steel.csv', sep='\t', index_col='time', encoding="utf-8")

df = my.rename_col(df, samples)

df = df.diff()
df = -df[df < 0]
df = df.fillna(0)

# df['time'] = df['time'].cumsum()

square = 1  # cm^2
measure = 10**(-3)/(10**(-4))  # з г/см^2 в кг/м^2

df = df / square * measure  # рахуємо інтенсивність
df_comp = pd.DataFrame(df.sum(), columns=['times'])
df_comp['times'] = df_steel['сталь 45'][120] / df_comp['times']
df = df.cumsum()
df_comp = df_comp.round(1)

df_comp.to_csv(my.dir_output+"wear_comparison.csv", index=True, index_label='sample', sep='\t', encoding='utf-8')
df.to_csv(my.dir_output+"wear_intens.csv", index=True, sep='\t', encoding='utf-8')
df_steel.to_csv(my.dir_output+"wear_intens_steel.csv", index=True, sep='\t', encoding='utf-8')