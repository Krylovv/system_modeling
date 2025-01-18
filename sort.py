import pandas as pd
import numpy as np


class DfSort:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.p = {'0,05': 1.984, '0,01': 2.626, '0,001': 3.390}

    def get_df(self):
        return self.df

    def remove_factor(self, factor_name):
        self.df = self.df.drop(factor_name, axis=1)

    def get_columns(self):
        return list(self.df.columns)[1:len(list(self.df.columns)) - 1]

    def factor_set_selector(self):
        factors = list(self.df.columns)[1:len(list(self.df.columns)) - 1]
        i = 0
        print('Выберите фактор:')
        for factor in factors:
            i += 1
            print(f'{i}: {factor}')
        n = int(input())
        return factors[n - 1]

    def get_stat_significance(self) -> list:
        # Извлекаем данные из DataFrame
        X = self.df[self.factor_set_selector()].values.reshape(-1, 1)
        y = self.df['Response'].values
        # Добавляем константу к матрице X
        X = np.hstack((np.ones((len(X), 1)), X))
        # Выполняем линейную регрессию
        beta, sse, sigma_squared = self.linear_regression(X, y)
        # Рассчитываем коэффициенты Стьюдента
        t_stats = self.calculate_t_statistics_for_df(beta, X, sigma_squared)
        return t_stats

    def linear_regression(self, X, y):
        # Решение системы методом наименьших квадратов
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        print(f'!!!!!{beta}')
        # Остатки
        residuals = y - X @ beta
        # Сумма квадратов остатков
        sse = np.sum(residuals ** 2)
        # Количество наблюдений
        n = len(y)
        # Количество независимых переменных (включая константу)
        k = X.shape[1]
        # Дисперсия остатков
        sigma_squared = sse / (n - k)
        return beta, sse, sigma_squared

    def calculate_t_statistics_for_df(self, beta, X, sigma_squared):
        # Количество наблюдений
        n = len(X)
        # Количество независимых переменных (включая константу)
        k = X.shape[1]
        # Ковариационная матрица оценок параметров
        cov_beta = sigma_squared * np.linalg.inv(X.T @ X)
        # Стандартные ошибки оценок параметров
        se_beta = np.sqrt(np.diag(cov_beta))
        # Коэффициенты Стьюдента
        t_values = beta / se_beta
        return t_values

    def compare_t_result(self):
        print('Рассчет коэффициента Стьюдента')
        print('Выберите уровень значимости:')
        keys = list(self.p.keys())
        i = 0
        for key in keys:
            i += 1
            print(str(i) + ': ' + key)
        significance = keys[int(input()) - 1]
        t_coef = self.get_stat_significance()[1]
        p_value = self.p[significance]
        print(f'Значение коэффициента Стьюдента для x составляет {t_coef: .3f}, табличное значение '
              f'значимости {significance} составляет {p_value}.')
        if t_coef > p_value:
            print('Рассчитанный коэффициент Стьюдента превышает табличное значение\n\n\n')
        else:
            print('Рассчитанный коэффициент Стьюдента ниже табличного значения\n\n\n')

    def get_correlation_coefficient(self):
        print('Рассчет коэффициента корреляции')
        a = str(input('Выберите формат\n1: Корреляция между факторами\n2: Корреляция между фактором и откликом\n'))
        columns_to_correlate = []
        if a == '1':
            print('\nВыберите два фактора для рассчета:\n')
            columns_to_correlate.append(self.factor_set_selector())
            columns_to_correlate.append(self.factor_set_selector())
            correlation = self.df[columns_to_correlate].corr(method='pearson')
            return correlation.iloc[0][columns_to_correlate[1]]
        elif a == '2':
            print('\nВыберите фактор для рассчета:\n')
            columns_to_correlate.append(self.factor_set_selector())
            columns_to_correlate.append('Response')
            correlation = self.df[columns_to_correlate].corr(method='pearson')
            print(f'Коэффициент корреляции: {correlation.iloc[0]["Response"]}')
            return correlation.iloc[0]['Response']
        else:
            print('Неверные входные данные')
            pass
