# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
import matplotlib as mpl
import pandas as pd
import numpy as np
import my_functions_for_diplom as my


def plot_data(dataframe, filename, ylistticks, Y_label):
    """"""

    ax=dataframe.plot(kind="bar", colormap='Accent', fontsize=14, yticks=ylistticks, figsize=(6,3))
    filename = "figures/" + filename
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005), fontSize=14)

    plt.ylabel(Y_label, size=14)
    plt.xlabel('Зразок', size=14)
    plt.xticks(rotation='horizontal', size=14)

    plt.legend(prop={'size':14})
    plt.axes().set_aspect('auto')
    plt.tight_layout(0)
    plt.savefig(filename + ".pdf", format="pdf")
    plt.clf()
    return

mpl.use("pgf")
pgf_with_custom_preamble = {
    "figure.figsize": (6, 3),
    "font.family": "serif",  # use serif/main font for text elements
    "text.usetex": True,  # use inline math for ticks
    "pgf.rcfonts": False,  # don't setup fonts from rc parameters
    "pgf.preamble": [
        #"\\usepackage[utf8]{inputenc}",
        "\\usepackage[no-math]{fontspec}",
        "\\usepackage{mathspec}",
        "\\usepackage{units}",         # load additional packages
        "\\usepackage{metalogo}",
        #"\\usepackage{unicode-math}",  # unicode math setup
        r"\setmathfont(Digits,Latin,Greek)[Scale=0.976, Numbers={Lining,Proportional}]{Times New Roman}",
        r"\setmainfont[Scale=0.976]{Times New Roman}",  # serif font via preamble
        ]
}
mpl.rcParams.update(pgf_with_custom_preamble)
import matplotlib.pyplot as plt

samples = my.decode()
inv_dict = {v: k for k, v in samples.items()}
line_style = [':', '-', '--', '-.']
df = pd.read_csv(my.dir_output+"hard.csv", sep='\t', header=0, encoding="utf-8")
df_wear = pd.read_csv(my.dir_output+"wear_intens.csv", sep='\t',index_col='time', header=0, encoding="utf-8")
df_wear_steel = pd.read_csv(my.dir_output+"wear_intens_steel.csv", sep='\t',index_col='time', header=0, encoding="utf-8")

for sample in samples.values():
    file = my.dir_output+'gravi_cumsum_'+sample+'.csv'
    df_grav = pd.read_csv(file, sep='\t', header=0, encoding="utf-8")

    # PLOTTING GRAV ANALISYS
    y_ticks = np.arange(-0.018, 0.006, 0.002)
    error = 0.0005
    pltname = 'figures/plt_gravi_' + sample
    df_grav['k'].plot(color='k', linestyle=line_style[0], yerr=error)
    df_grav['W'].plot(color='k', linestyle=line_style[1], yerr=error)
    df_grav['Cr'].plot(color='k', linestyle=line_style[2], yerr=error)
    df_grav['C'].plot(color='k', linestyle=line_style[3], yerr=error)
    plt.legend()
    plt.axhline(y=0, linewidth=1, color='k')
    plt.grid()
    plt.xticks(list(range(10)), size=14)
    plt.yticks(y_ticks, size=14)
    plt.ylabel(r'Ерозія (приріст) $\sum \Delta m$, $\frac{\text{г}}{\text{см}^2}$', size=14)
    plt.xlabel('Час, хв', size=14)
    plt.tight_layout(0)
    plt.axes().set_aspect('auto')
    plt.savefig(pltname + ".pdf", format="pdf")
    plt.clf()

    # PLOT HARDNESS
    df.plot.scatter(x='depth', y=sample, color='k', yerr=1, xerr=2)
    plt.grid()
    plt.ylabel('Мікротвердість, ГПа', size=14)
    plt.xlabel('Глибина, мкм', size=14)
    plt.yticks(size=14)
    plt.xticks(size=14)
    plt.tight_layout(0)
    plt.savefig("figures/plt_hard_" + sample + ".pdf", format="pdf")
    plt.clf()

    # PLOT WEAR GRAFS
    error = 0.005
    pltname = 'figures/plt_wear_'+sample
    df_wear[sample].plot(color='k', linestyle=line_style[0], yerr=error)
    df_wear_steel['сталь 45'].plot(color='k', linestyle=line_style[1], yerr=error)
    plt.legend()
    #plt.axhline(y=0, linewidth=1, color='k')
    plt.grid()
    plt.xticks(list(df_wear_steel.index.values), size=14)
    plt.yticks(size=14)
    plt.ylabel(r'Інтенсивність зносу, $\frac{\textup{кг}}{\textup{м}^2}$', size=14)
    plt.xlabel('Час, хв', size=14)
    plt.tight_layout(0)
    plt.axes().set_aspect('auto')
    plt.savefig(pltname + ".pdf", format="pdf")
    plt.clf()

### COMPARISON ###

# OPEN FILES
df_hard_comp = pd.read_csv(my.dir_output+"hard_comparison.csv",
                           index_col='sample',
                           sep='\t',
                           encoding="utf-8")
df_wear_comp = pd.read_csv(my.dir_output+"wear_comparison.csv",
                           index_col='sample',
                           sep='\t',
                           encoding="utf-8")
df_grav_comp = pd.read_csv(my.dir_output+"gravi_eff.csv",
                           index_col=0,
                           sep='\t',
                           encoding="utf-8")
df_grav_comp= df_grav_comp.transpose().round(1)
df_wh_comp = pd.concat([df_wear_comp, df_hard_comp], axis=1)


df_hard_comp['max_hard'] = df_hard_comp['max_hard']/2.4
df_hard_comp['max_hard'] = df_hard_comp['max_hard'].round(1)
df_wh = pd.concat([df_wear_comp, df_hard_comp], axis=1)
df_wh = df_wh.rename(columns={"max_hard": r'$\frac{\mu H\textup{(зразок)}}{\mu H\textup{(сталь 45)}}$',
                              "times": r'$\frac{\textup{I(сталь 45)}}{\textup{I(зразок)}}$'})
# PLOT HARDNESS AND WEAR
plot_data(df_wh,
          "comp_wh",
          list(range(0, 30, 5)), r'Покращення властивості, рази')
plot_data(df_grav_comp,
          "comp_grav",
          list(range(0,55,5)), r'Коефіцієнт ефективності, в.од.')
