# -*- coding: utf-8 -*-
import pandas as pd
import statistics as stat
import tabulate as tab
import math
data = pd.read_csv('ave_1.csv', delimiter=';')
average = data["hardness"].mean()
median = data["hardness"].median()
data_round = data["hardness"].round()
mode = data_round.mode().mean()
dispersion = data["hardness"].var()
SKO = data["hardness"].std()
delta = SKO/math.sqrt(len(data))
delta = "%.2f" % delta
average = "%.2f" % average
dispersion = "%.2f" % dispersion
SKO = "%.2f" % SKO
delta = u'$\pm' + delta +u'$'
table_stat = [
[u'Середнє значення',average],
[u'Медіана',median],
[u'Мода',mode],
[u'Дисперсія',dispersion],
[u'СКВ',SKO],
[u'Похибка',delta]
]
del(tab.LATEX_ESCAPE_RULES[u'$'])
del(tab.LATEX_ESCAPE_RULES[u'\\'])
mystring = tab.tabulate(table_stat, headers={u'Значення, ГПа'}, tablefmt="latex", floatfmt=".2f")
fout = open('table_stat.tex','w')
fout.write(mystring.encode('utf8'))
fout.close() 
