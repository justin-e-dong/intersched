import os
import numpy as np
import matplotlib.pyplot as plt
from base import DATA_DIR, TRACE_DIR

trace_path = f"{DATA_DIR}/{TRACE_DIR}"

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

# 177 x 176
# rows x cols

ints_sum_across_cores = np.sum(snapshots, 2)

# base = ints_sum_across_cores[0]
# res = np.subtract(ints_sum_across_cores, base)
base = ints_sum_across_cores[0].reshape(1, -1)
shifted = np.concatenate((base, ints_sum_across_cores))[:-1]
int_rate = np.subtract(ints_sum_across_cores, shifted)

# plot the interrupt rate, rather than the number of interrupts
# (change from the previous collection of interrupts)
