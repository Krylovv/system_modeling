import pandas as pd
import numpy as np

# Генерация случайных данных
np.random.seed(42)  # Устанавливаем фиксированное значение для воспроизводимости результата

# Количество наблюдений
n = 100

# Создаем временную серию
time_series = pd.date_range(start='2023-01-01', periods=n, freq='D')

# Генерация случайных факторов
factor1 = np.random.normal(loc=10, scale=2, size=n)
factor2 = np.random.normal(loc=20, scale=3, size=n)
factor3 = np.random.normal(loc=30, scale=4, size=n)
factor4 = np.random.normal(loc=1000, scale=5, size=n)

# Генерация отклика, зависящего от факторов
response = 5 + 2*factor1 + 3*factor2 + 4*factor3 + np.random.normal(scale=5, size=n)

# Создание DataFrame
df = pd.DataFrame({
    'Date': time_series,
    'Factor1': factor1,
    'Factor2': factor2,
    'Factor3': factor3,
    'Factor4': factor4,
    'Response': response
})

# Сохраняем DataFrame в CSV-файл
df.to_csv('generated_data.csv', index=False)
print("CSV файл успешно создан!")