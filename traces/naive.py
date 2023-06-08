import sys
import random
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import math
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from clean_data import *

input_file = sys.argv[1] + ".log"
output_name = sys.argv[1]
title_name = sys.argv[2]

def parse_data(input_file):
    data = clean_data(input_file)
    parsed_data = []
    for line in data:
        parts = line.split(',')
        irq = int(parts[0].split(':')[1].strip())
        entry_time = float(parts[1].split(':')[1].strip())
        exit_time = float(parts[2].split(':')[1].strip())
        parsed_data.append((irq, entry_time, exit_time))
    df = pd.DataFrame(parsed_data, columns=["IRQ", "Entry", "Exit"])
    # df["Entry"] = pd.to_datetime(df["Entry"], unit="s")
    # df["Exit"] = pd.to_datetime(df["Exit"], unit="s")
    return df

def calculate_mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

df = parse_data(input_file)

# Split into train and test sets
X = df["Entry"].values
size = int(len(X) - 800)
train, test = X[0:size], X[size:len(X)]

window_sizes = [10, 20, 100, 200]

for window_size in window_sizes:

    predictions = []

    # Make predictions
    for i in range(0, len(test)):

        predictions.append(X[i + size - window_size])

    # Evaluate forecasts
    rmse = math.sqrt(mean_squared_error(test, predictions[:len(test)]))
    print('Test RMSE: %.3f' % rmse)

    mape = calculate_mape(test, predictions[:len(test)])
    print("Test MAPE for " + title_name + " Naive with Window of " + str(window_size) + ": %.3f%%" % mape)

    # Plot forecasts against actual outcomes
    plt.figure()
    ax = plt.axes()
    ax.plot(test, color='blue', label='Actual')
    ax.plot(predictions, color='red', label='Prediction')
    ax.set_xlabel('Number of Interrupts')
    ax.set_ylabel('Time from Start (s)')
    ax.set_title(title_name + " Naive Interrupt Predictions with Window of " + str(window_size))
    ax.legend()
    plt.show()
    plt.savefig("./output/" + output_name + "_naive_" + "window" + str(window_size) + ".pdf")