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
X = df["Exit"].values
size = int(len(X) * 0.95)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]

predictions = []

# Make predictions
for t in range(len(test)):
    model = ARIMA(history, order=(1, 1, 1))
    model_fit = model.fit()
    
    forecast = model_fit.forecast()
    yhat = forecast[0]
    predictions.append(yhat)
    
    history.append(test[t])

# Evaluate forecasts
rmse = math.sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)

mape = calculate_mape(test, predictions)
print('Test MAPE: %.3f%%' % mape)

# Plot forecasts against actual outcomes
plt.plot(test)
plt.plot(predictions, color='red')
plt.show()
plt.savefig("./" + output_name + "_arima.pdf")