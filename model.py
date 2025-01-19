import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class Model:
    def __init__(self, df: pd.DataFrame, factors=None):
        # Создание модели при инициализации
        if factors is None:
            factors = ['Factor1', 'Factor2', 'Factor3', 'Factor4']
        X = df[factors]
        y = df['Response']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.X_test = X_test
        self.y_test = y_test
        # Обучение модели
        model = LinearRegression()
        model.fit(X_train, y_train)
        self.model = model
        print('Построена модель множественной линейной регрессии')
        self.coefficients = model.coef_
        self.intercept = model.intercept_
        # Предсказание на тестовой выборке
        y_pred = model.predict(X_test)
        # Оценка качества модели
        self.mae = mean_absolute_error(y_test, y_pred)
        self.mse = mean_squared_error(y_test, y_pred)
        count = 0
        for i in range(len(list(y_pred))):
            count += abs((list(y_test)[i] - list(y_pred)[i])/list(y_test)[i])
        # Коэффициент детерминации
        self.r2 = r2_score(y_test, y_pred)
        # Оценка значимости коэффициента детерминации
        self.f = (self.r2 / len(factors)) / ((1 - self.r2) / (len(y_pred) - len(factors) - 1))
        # Средняя ошибка аппроксимации
        self.mape = count / len(list(y_pred)) * 100

    def get_coefficients(self):
        return self.coefficients, self.intercept

    def print_coefficients(self):
        cf = self.get_coefficients()
        print(f'Коэффициенты переменных: {cf[0]}')
        print(f'Свободный член: {cf[1]}\n')

    def get_stats(self):
        return self.mae, self.mse, self.r2

    def print_stats(self):
        stats = self.get_stats()
        print(f'Средняя абсолютная ошибка: {stats[0]}')
        print(f'Среднеквадратическая ошибка: {stats[1]}')
        print(f'Коэффициент детерминации: {stats[2]}\n\n')

    def mean_absolute_percentage_error(self, y_true, y_pred):
        return 100 * np.mean(np.abs((y_true - y_pred) / y_true))

    def get_evaluation(self):
        return self.f, self.mape

    def print_evaluation(self):
        ev = self.get_evaluation()
        print(f'Оценка коэффициента детерминации на статистическую значимость: {ev[0]}')
        print(f'Средняя ошибка аппроксимации: {ev[1]}')
        if ev[0] > 2.36:
            print('Модель адекватна')

    def get_prediction(self, factors: list):
        coeffs = self.get_coefficients()
        value = 0
        for i in range(len(factors)):
            value += float(factors[i]) * coeffs[0][i]
        value += coeffs[1]
        return value

    def get_special_values(self):
        # Базовые необходимые параметры
        mean_x = np.mean(self.X_test)
        mean_y = np.mean(self.y_test)
        beta_list = self.coefficients

        # Расчет коэффициента эластичности
        elasticity = []
        for beta in beta_list:
            elasticity.append(beta * (mean_x/mean_y))

        # Расчет меры вариации результативного признака
        elasticity_squared_list = []
        for value in elasticity:
            elasticity_squared_list.append(value * value)

        # Расчет системного эффекта факторов
        elasticity_squared_sum = 0
        for value in elasticity:
            elasticity_squared_sum += value * value
        system_effect = self.r2 - elasticity_squared_sum

        return elasticity, elasticity_squared_list, system_effect

    def print_special_values(self):
        values = self.get_special_values()
        print(f'Коэффициент эластичности: {values[0]}')
        print(f'Мера вариации результативного признака: {values[1]}')
        print(f'Показатель системного эфекта факторов: {values[2]}')
