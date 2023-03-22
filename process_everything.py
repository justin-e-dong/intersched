import os
import json
import numpy as np
import matplotlib.pyplot as plt
from base import DATA_DIR, TRACE_DIR

#############################
# process_data_1_interrupt.py
#############################

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

# only look at a small subset of the data
file_paths = file_paths[0:4]

for file_path in file_paths:
    with np.load(file_path) as res:
        snapshots = res["snapshots"]
        times = res["times"]
        all_snapshots.append(snapshots)
        all_times.append(times)

snapshots = np.concatenate(all_snapshots)
times = np.concatenate(all_times)

cal_index = -1
for (i, l) in enumerate(row_labels):
    if l == "CAL":
        cal_index = i

snapshots = snapshots[:, cal_index:(cal_index+1), :]
print(snapshots.shape)

# 177 x 176
# rows x cols
# (177 interrupts) x (176 cores)

ints_sum_across_cores = np.sum(snapshots, 2)

def compute_change(arr):
    base = arr[0]
    arr_shape = list(arr.shape)
    arr_shape[0] = 1
    base = base.reshape(tuple(arr_shape))
    shifted = np.concatenate((base, arr))[:-1]
    change = np.subtract(arr, shifted)
    return change[1:]

# base = ints_sum_across_cores[0]
# res = np.subtract(ints_sum_across_cores, base)

ints_change = compute_change(ints_sum_across_cores)
time_change = compute_change(times)

time_change_s = np.multiply(time_change, 1e-9)

time_change_rep = time_change_s.reshape(-1, 1)
time_change_rep = np.repeat(time_change_rep, ints_change.shape[1], axis=1)
ints_rate_s = ints_change / time_change_rep

plot_times = times - times[0]
plot_times = np.multiply(plot_times, 1e-9)
plot_times = plot_times[1:]

print('Done processing, displaying plot now')

plt.plot(plot_times, ints_rate_s)

plt.title("Interrupt Rate (All cores)")

plt.xlabel('Time (s)')
plt.ylabel('Interrupt Rate (ints/s)')

plt.legend(loc='upper right')
plt.savefig(data_dir + "/all_interrupts.png")
plt.show()

'''
final_str = ""
ints_rate_s = ints_rate_s.reshape(-1)
for i in range(ints_rate_s.shape[0]):
    # t = plot_times[i].item()
    v = ints_rate_s[i].item()
    final_str += f"{i}\t{v}\n"

with open("cal_seq.txt", "w") as f:
    f.write(final_str)
'''

#############################
# process_data_per_cpu.py
#############################

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

# only look at a small subset of the data
file_paths = file_paths[0:10]

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
# (177 interrupts) x (176 cores)

ints_sum_across_interrupt_types = np.sum(snapshots, 1)

def compute_change(arr):
    base = arr[0]
    arr_shape = list(arr.shape)
    arr_shape[0] = 1
    base = base.reshape(tuple(arr_shape))
    shifted = np.concatenate((base, arr))[:-1]
    change = np.subtract(arr, shifted)
    return change[1:]

# base = ints_sum_across_cores[0]
# res = np.subtract(ints_sum_across_cores, base)

ints_change = compute_change(ints_sum_across_interrupt_types)
time_change = compute_change(times)

time_change_s = np.multiply(time_change, 1e-9)

time_change_rep = time_change_s.reshape(-1, 1)
time_change_rep = np.repeat(time_change_rep, ints_change.shape[1], axis=1)
ints_rate_s = ints_change / time_change_rep

plot_times = times - times[0]
plot_times = np.multiply(plot_times, 1e-9)
plot_times = plot_times[1:]

# print(ints_rate_s)
# print(plot_times)

# plot the interrupt rate, rather than the number of interrupts
# (change from the previous collection of interrupts)

overall_rate_mean = np.mean(ints_rate_s[0:1000])
print(f"Overall Interrupt Rate Mean per CPU: {overall_rate_mean}")

# print(labels)
print('Done processing, displaying plot now')

plt.plot(plot_times, ints_rate_s)

plt.title("Interrupt Rate For Each CPU")

plt.xlabel('Time (s)')
plt.ylabel('Interrupt Rate (ints/s)')

plt.legend(loc='upper right')
plt.savefig(data_dir + "/interrupts_per_cpu.png")
plt.show()

#############################
# process_data.py
#############################

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

# only look at a small subset of the data
file_paths = file_paths[0:10]

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
# (177 interrupts) x (176 cores)

ints_sum_across_cores = np.sum(snapshots, 2)

def compute_change(arr):
    base = arr[0]
    arr_shape = list(arr.shape)
    arr_shape[0] = 1
    base = base.reshape(tuple(arr_shape))
    shifted = np.concatenate((base, arr))[:-1]
    change = np.subtract(arr, shifted)
    return change[1:]

# base = ints_sum_across_cores[0]
# res = np.subtract(ints_sum_across_cores, base)

ints_change = compute_change(ints_sum_across_cores)
time_change = compute_change(times)

time_change_s = np.multiply(time_change, 1e-9)

time_change_rep = time_change_s.reshape(-1, 1)
time_change_rep = np.repeat(time_change_rep, ints_change.shape[1], axis=1)
ints_rate_s = ints_change / time_change_rep

plot_times = times - times[0]
plot_times = np.multiply(plot_times, 1e-9)
plot_times = plot_times[1:]

# print(ints_rate_s)
# print(plot_times)

# plot the interrupt rate, rather than the number of interrupts
# (change from the previous collection of interrupts)

ints_change_sum = np.sum(ints_change, axis=0)

k = 6
topk_inds = np.argpartition(ints_change_sum, -k)[-k:]
choose_inds = topk_inds
# all_non_zero_indices = np.where(np.all(ints_change != 0, axis=0))[0]
# choose_inds = all_non_zero_indices

choose_inds = np.sort(choose_inds)

ints_rate_s_filtered = np.take(ints_rate_s, choose_inds, axis=1)

z_ind_set = set(choose_inds)
labels = []
for (i, l) in enumerate(row_labels):
    if i in z_ind_set:
        labels.append(l)

sums_filtered = np.take(ints_sum_across_cores, choose_inds, axis=1)

print(labels)
print('Done processing, displaying plot now')

plt.plot(plot_times, ints_rate_s_filtered, label=labels)

plt.title("Interrupt Rate Totalled Across Cores")

plt.xlabel('Time (s)')
plt.ylabel('Interrupt Rate (ints/s)')

plt.legend(loc='upper right')
plt.savefig(data_dir + "/top_6_interrupts.png")
plt.show()