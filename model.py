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
        # Обучение модели
        model = LinearRegression()
        self.model = model.fit(X_train, y_train)
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
        self.mape = count / len(list(y_pred)) * 100
        # Коэффициент детерминации
        self.r2 = r2_score(y_test, y_pred)

    def get_coefficients(self):
        return self.coefficients, self.intercept

    def print_coefficients(self):
        cf = self.get_coefficients()
        print(f'Коэффициенты переменных: {cf[0]}')
        print(f'Свободный член: {cf[1]}\n')

    def get_stats(self):
        return self.mae, self.mse, self.mape, self.r2

    def print_stats(self):
        stats = self.get_stats()
        print(f'Средняя абсолютная ошибка: {stats[0]}')
        print(f'Среднеквадратическая ошибка: {stats[1]}')
        print(f'Средняя ошибка аппроксимации: {stats[2]}')
        print(f'Коэффициент дисперсии: {stats[3]}\n\n')

    def mean_absolute_percentage_error(self, y_true, y_pred):
        return 100 * np.mean(np.abs((y_true - y_pred) / y_true))
