import os
import json
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from base import DATA_DIR, TRACE_DIR

data_dir = DATA_DIR
trace_path = f"{data_dir}/{TRACE_DIR}"

row_labels = None
with open(f"{data_dir}/row_labels.json") as f:
    row_labels = json.load(f)

all_snapshots = []
all_times = []

file_paths = []
for dir_entry in os.scandir(trace_path):
    name = dir_entry.name
    file_path = f"{trace_path}/{name}"
    file_paths.append(file_path)

file_paths.sort()

for file_path in file_paths:
    with np.load(file_path) as res:
        snapshots = res["snapshots"]
        times = res["times"]
        all_snapshots.append(snapshots)
        all_times.append(times)

snapshots = np.concatenate(all_snapshots)
times = np.concatenate(all_times)

ints_sum_across_cores = np.sum(snapshots, 2)

def compute_change(arr):
    base = arr[0]
    arr_shape = list(arr.shape)
    arr_shape[0] = 1
    base = base.reshape(tuple(arr_shape))
    shifted = np.concatenate((base, arr))[:-1]
    change = np.subtract(arr, shifted)
    return change[1:]

ints_change = compute_change(ints_sum_across_cores)
time_change = compute_change(times)

time_change_s = np.multiply(time_change, 1e-9)

time_change_rep = time_change_s.reshape(-1, 1)
time_change_rep = np.repeat(time_change_rep, ints_change.shape[1], axis=1)
ints_rate_s = ints_change / time_change_rep

# times
plot_times = times - times[0]
plot_times = np.multiply(plot_times, 1e-9)
plot_times = plot_times[1:]

ints_change_sum = np.sum(ints_change, axis=0)

k = 1
topk_inds = np.argpartition(ints_change_sum, -k)[-k:]
choose_inds = topk_inds

choose_inds = np.sort(choose_inds)

# highest interrupt rate
ints_rate_s_filtered = np.take(ints_rate_s, choose_inds, axis=1)

#############
# Arima Model
#############

# https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/ 

# initialize dataframe
# plot_times = np.expand_dims(plot_times, axis=1)
# concatenated = np.concatenate((plot_times, ints_rate_s_filtered), axis=1)
# df = pd.DataFrame(concatenated, columns =['time', 'interrupt rate'])
df = pd.DataFrame(ints_rate_s_filtered, columns =['interrupt rate'])

# split into train and test sets
X = df.values
size = int(len(X) * 0.9990)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]

model = ARIMA(history, order=(5,1,0))
model_fit = model.fit()
predictions = model_fit.forecast(len(test))

# evaluate forecasts
rmse = math.sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)

# plot forecasts against actual outcomes
plt.plot(test)
plt.plot(predictions, color='red')
plt.show()
plt.savefig(data_dir + "/arima_model.png")