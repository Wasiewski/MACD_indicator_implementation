import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import datetime as DT
from matplotlib import dates

file_to_explore = "C://Users//oskar//OneDrive//Pulpit//Nowy folder//macd//dane.csv"
# path to your csv data

df = pd.read_csv(file_to_explore)
samples = df['Close']

initial_value = 1000*samples[0]
print("Initial value of samples equals:", initial_value)
unit = 1000
cash = 0
stock_price = 0
maximun_cash = 65000


def ema(values, current_day, windows):
    a = 0
    b = 0
    one_minus_alpha = 1.0 - (2.0/(windows+1))
    for i in range(0, windows):
        tem = pow(one_minus_alpha, i)
        if(current_day - i > 0):
            a += tem * values[current_day-1-i]
        else:
            a += tem*values[0]
        b += tem
    return a/b


def calculateMacd(samples, current_day):
    return ema(samples, current_day, 12)-ema(samples, current_day, 26)


def macd_signal(samples, current_day):

    return ema(samples, current_day, 9)


def buy(currenDayPrice, day):
    global cash
    global unit

    if unit == 0:  # I can buy if there was a sale before
        global stock_price
        stock_price = currenDayPrice   # the share price on the day we bought it
        unit = unit + cash/currenDayPrice
        print("buy", unit)
        cash = cash % currenDayPrice
        print(f'day {day} after buying {cash}')
    else:
        print("You are lack of funds to buy, need to wait!")


def sell(currentDayPrice, day):
    global unit
    global cash
    global stock_price
    global maximun_cash
    if unit != 0:
        print("sell ", unit)
        stock_price = 0
        cash = cash + unit*currentDayPrice
        if cash > maximun_cash:
            maximun_cash = cash
            print(f'day {day} sell {cash}')
            unit = 0


def show_credentials(macd_samples, signal_samples):
    global cash
    financial_profit = cash
    print("Cash rest : ", financial_profit)
    print("unit ", unit)
    print("max cash", maximun_cash)
    print("Financial profit:", maximun_cash-initial_value)

    fig, ax = plt.subplots(figsize=(16, 16))

    ax.plot(samples[:998].index, macd_samples, label='MACD')
    ax.plot(samples[:998].index, signal_samples, label='Signal')

    ax.set_xlabel('day number')

    ax.legend()

    plt.figure(figsize=(7, 12))
    plt.subplot(2, 1, 1)

    plt.plot(samples[:998].index, df['Close'])

    plt.grid(True)

    plt.show()


def strategy():

    macd_samples = []
    signal_samples = []
    hist = []
    for i in range(0, len(samples)):
        macd_samples.append(samples[i])
        signal_samples.append(samples[i])
        hist.append(0)

    for i in range(1, len(samples)):
        macd_samples[i-1] = calculateMacd(samples, i)
        signal_samples[i-1] = macd_signal(macd_samples, i)
        hist[i-1] = macd_samples[i-1]-signal_samples[i-1]

    for i in range(1, len(samples)):
        if hist[i-1] > hist[i] and hist[i] > 0:  # we're sure the histogram will be positive
            if stock_price < samples[i] or stock_price == 0:
                # if stock_price in day we bought is lower or equal with current price we sell,incase of colapse
                sell(samples[i], i)
        elif hist[i-1] < hist[i] and hist[i] < 0:  # we have an upward trend,time to buy
            # if stock_price < samples[i] or stock_price==0:
            buy(samples[i], i)

    show_credentials(macd_samples, signal_samples)


strategy()
