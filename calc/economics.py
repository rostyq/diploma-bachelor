# -*- coding: utf-8 -*-

import pandas as pd
import my_functions_for_diplom as my


def cost_round(x):
    return round(x, 2)


# Витрати на оплату праці

file_stuff = my.dir_data+'eco_stuff.csv'  # дані з зарплатами
file_mat = my.dir_data+'eco_mat.csv'  # дані з витратами матеріалів
average_days = 21  # сер-ня к-сть робочих днів у місяці

# зчитування файлу та заповнення пустих даних
df_stuff = pd.read_csv(file_stuff, sep='\t', encoding="utf-8")
df_stuff = df_stuff.fillna(0)

# розрахунок плати працівникам за день
df_stuff['salary per day'] = df_stuff.salary / average_days

# підрахунок суми годин
#col = ['analysis', 'dev_method', 'preparation', 'experiment', 'discussion']
df_stuff['sum time'] = pd.DataFrame(df_stuff.drop(['salary', 'name', 'salary per day'], 1).transpose().sum())

# підрахунок фонду зар.плати та єдиного соц.внеску
wage_bill = round(sum(df_stuff['salary per day'] * df_stuff['sum time']), 2)
social = round(0.22 * wage_bill, 2)

# Витрати на матеріали

# зчитування файлу та заповнення пустих даних
df_mat = pd.read_csv(file_mat, sep='\t', encoding="utf-8", index_col='name')
df_mat = df_mat.fillna(0)

df_mat['sum'] = df_mat['count'] * df_mat['cost']  # рахуємо витрати на кожен матеріал
mat_sum_cost = df_mat['sum'].sum()  # витрати на всі матеріали
trans_cost = mat_sum_cost * 0.1  # Транспортно-заготівельні витрати
mat_cost = mat_sum_cost + trans_cost  # Повна сума витрат на матеріали

# Інші прямі невраховані та накладні витрати

other = (wage_bill + mat_cost + social) * 0.1
overhead = (wage_bill + mat_cost + social + other) * 0.2

# формуємо таблицю даних
data_cost = pd.DataFrame([[wage_bill], [social], [mat_cost], [other], [overhead]],
                         index=['ФЗП', 'Соц. внесок', 'Матеріали', 'Інші витрати', 'Накладні витрати'],
                         columns=['Сума'])

# рахуємо відсоткове співвідношення
data_cost['%'] = data_cost['Сума'] / data_cost['Сума'].sum() * 100
data_cost.loc['Всього'] = data_cost.sum()

# Науково-технічна ефективність НДР

k1, k2, k3, k4 = 1, 10, 5, 5
grade = k1 * k2 * k3 * k4  # Бальна оцінка економічної ефективності

# Умовний річний економічний ефект науково-дослідної роботи
En = 0.2  # для нашого розрахунку обираємо 0.2
economic_effect = 500 * grade - En * data_cost['Сума'].loc['Всього']

# Таким чином, умовний економічний ефект становить
economic_benefit = round(economic_effect / data_cost['Сума'].loc['Всього'], 2)
data_cost = data_cost.apply(cost_round)  # округляємо до 2-го знаку

# вивід даних
print(df_stuff, '\n')
print(df_mat, '\nCума по матеріалам: %s.\n' % df_mat['sum'].sum())
print(data_cost, '\n')
print('''Бальна оцінка: %s.
Ефективність НДР: %s.
Умовний економічний ефект: %s''' % (grade, economic_benefit, round(economic_effect, 2)))
