import yfinance as yf
from statsmodels.tsa.holtwinters.model import ExponentialSmoothing
import matplotlib.pyplot as plt


def get_gold_prices(ticker, start_date, end_date):
    gold_data = yf.download(ticker, start=start_date, end=end_date)
    return gold_data


def data_transform(df):
    monthly_mean = df.resample('M').mean()
    return monthly_mean


def holt_winters_forecast(train_data, test_data, seasonal_periods=12):
    train_series = train_data['Close']
    # Создание модели Хольта-Уинтерса
    model = ExponentialSmoothing(
        train_series,
        trend='add',  # Добавляемый тренд
        seasonal='add',  # Аддитивная сезонность
        seasonal_periods=seasonal_periods  # Длина сезона
    )
    fit_model = model.fit()
    # Прогноз
    forecast = fit_model.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1)

    return fit_model.params, forecast


# Расчет для золота
ticker = 'GLD'
start_date = '2017-01-01'
end_date = '2023-12-31'
gold_prices = get_gold_prices(ticker, start_date, end_date)
monthly_gold_prices = data_transform(gold_prices)

# Разделение данных на обучающую и тестовую выборки
num_years = 6
num_months_per_year = 12
total_observations = num_years * num_months_per_year

train_data = monthly_gold_prices.iloc[:total_observations]
test_data = monthly_gold_prices.iloc[total_observations:total_observations + num_months_per_year]

params, forecast = holt_winters_forecast(train_data, test_data, seasonal_periods=num_months_per_year)

# Визуализация
plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data['Close'], label="Тренировочные данные")
plt.plot(test_data.index, test_data['Close'], label="Тестовые данные")
plt.plot(forecast.index, forecast, marker='o', markersize=8, label="Прогноз")
plt.title("Модель Хольта-Винтерса")
plt.xlabel("Месяц")
plt.ylabel("Средняя цена за месяц ($)")
plt.legend()
plt.grid(True)
plt.show()

print("Parameters of the model:", params)
