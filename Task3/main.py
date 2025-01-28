import random
import matplotlib.pyplot as plt

### Константы
Simulation_Period = int(input("Введите длительность симуляции в годах: "))
Random_Interest = round(10 * random.uniform(0.75, 1.25))
VAT_Rate = 0.2
VagesAndTaxes = 500
TransferVol = 30
TransferRate = 150
TransferDecision = 0
STOP_SELL = 0
Start_Rate = 10
Ret_Price = 100
RentRate = 200
OptOfferBaseVolume = 40
OptOfferAcceptDecision = 0
MeanDPrice = 100
Max_Demand = 30
Longevity = 10
Interest_Rate = Random_Interest
InitAccount = 10000
Credit_Sum = 10000
BasicOptOfferVol = 50
BasicOptOfferPrice = 35
CurTime = 0

### Уровни
ShopStore = 30
Debt = Credit_Sum
BasicStore = 80
All_Lost = 0
Account = InitAccount + Credit_Sum



overall_account = []
while CurTime < Simulation_Period:
    ### Пересчет переменных
    Percent_Payment = Debt * Interest_Rate / 1200
    Demand = round(Max_Demand * (1 - 1/(1 + pow(2.7183, (-0.05 * (Ret_Price - MeanDPrice))))))
    # print(f"!!!!!!!!!!!!!!!   {-0.05 * Ret_Price - MeanDPrice}")
    RND_Demand = round(Demand * random.uniform(0.7, 1.2))
    RndOfferVolume = round(OptOfferBaseVolume * random.uniform(0.75, 1.25))
    SoldRet = (1 - STOP_SELL) * min(RND_Demand, ShopStore)
    Income = Ret_Price * SoldRet
    Selling = SoldRet
    TransferActualVolume = min(BasicStore, TransferVol * TransferDecision) if Account > TransferRate else 0
    TransSpend = TransferRate if TransferActualVolume > 0 else 0
    VAT = Income * VAT_Rate
    YearlyPayment = 12 * (Interest_Rate / 1200) * pow((1 + (Interest_Rate / 1200)), (Longevity * 12)) / (
                pow((1 + (Interest_Rate / 1200)), (Longevity * 12)) - 1)
    GoodsTransfer = int(TransferActualVolume)
    Debt_Reduce = YearlyPayment - Percent_Payment
    Lost = ShopStore + GoodsTransfer - 100 if ShopStore + GoodsTransfer > 100 else 0
    DailySpending = min(RentRate + VagesAndTaxes, Account)
    BasicPriceRnd = BasicOptOfferVol * random.uniform(0.7, 1.3)
    AddPriceByTime = BasicOptOfferPrice * 0.03 * CurTime + BasicOptOfferPrice * 0.01 * CurTime * random.randrange(0, 1)
    OfferOnePrice = AddPriceByTime + BasicPriceRnd
    OfferFullPrice = OfferOnePrice * RndOfferVolume
    OfferAcceptPossibility = 1 if Account >= OfferFullPrice else 0
    SmallOptIncome = OfferAcceptPossibility * OptOfferAcceptDecision * RndOfferVolume
    Sp_Opt_Value = OfferFullPrice if OfferAcceptPossibility * OptOfferAcceptDecision > 0 else 0
    Spend_for_Offer = Sp_Opt_Value

    overall_account.append(Account)

    CurTime += 1
    print(f"Год симуляции: {CurTime}\n")
    print("--------------------------------")
    print("Оптовое предложение:")
    print(f"Объем партии: {RndOfferVolume}, цена партии: {OfferFullPrice}, цена за единицу: {OfferOnePrice}")
    print("--------------------------------")
    print("Склады:")
    print(f"Склад магазина: {ShopStore}, основной склад: {BasicStore}")
    print("--------------------------------")
    print("Торговля:")
    print(f"Текущий спрос: {RND_Demand}")


    ### Принятие решений
    OptOfferAcceptDecision = int(input("Принять оптовое предложение и закупиться 0/1 "))
    TransferDecision = int(input("Перевезти на склад магазина 0/1 "))
    if TransferDecision == 1:
        TransferVol = int(input("Введите объем перевозки: "))
    STOP_SELL = int(input("Остановить торговлю 0/1 "))

    ### Рассчет уровней
    All_Lost += Lost
    BasicStore += SmallOptIncome
    BasicStore -= GoodsTransfer
    Debt -= Debt_Reduce
    ShopStore += GoodsTransfer
    ShopStore -= Lost
    ShopStore -= Selling
    Account += Income
    Account -= VAT + TransSpend + Spend_for_Offer + YearlyPayment + DailySpending

    print(f"Потери: {All_Lost}")
    print(f"Товара в магазине: {ShopStore}")
    print(f"Товара на складе: {BasicStore}")
    print(f"Долг по кредиту: {Debt}")
    print(f"Сумма на счету: {Account}")

# Визуализация
plt.figure(figsize=(12, 6))
plt.plot(overall_account, label="Состояние счета")
plt.title("Account")
plt.xlabel("Год")
plt.ylabel("Сумма")
plt.legend()
plt.show()
