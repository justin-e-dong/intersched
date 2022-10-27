import json
import sys
import os
import time
from datetime import datetime
import numpy as np

DATA_DIR = "data"
TRACE_DIR = "traces"

def get_snapshot():
    full_data = None
    now = time.time_ns()
    with open("/proc/interrupts", "r") as f:
        full_data = f.read()

    lines = full_data.split("\n")
    lines = list(filter(lambda x: len(x) > 0, lines))
    col_labels = lines[0].split()
    row_labels = []
    res = []
    for line in lines[1:]:
        cols = line.split()
        row_labels.append(cols[0][:-1])
        line_res = []
        for c in cols[1:]:
            try:
                val = int(c)
                line_res.append(val)
            except Exception as e:
                break
        while (len(line_res) < len(col_labels)):
            line_res.append(0)
        res.append(line_res)

    if not os.path.exists(DATA_DIR):
        # make traces dir in data dir
        os.makedirs(f"{DATA_DIR}/{TRACE_DIR}")
        
        # dump labels if the data path doesn't exist
        with open(f"{DATA_DIR}/row_labels.json", "w") as f:
            json.dump(row_labels, f)

        with open(f"{DATA_DIR}/col_labels.json", "w") as f:
            json.dump(col_labels, f)

    print(len(row_labels))
    print(len(col_labels))

    return np.array(res), now

# interval in seconds
def collect_and_dump_trace(interval=1, count=100):
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    snapshots = []
    times = []
    for i in range(count):
        snap, t = get_snapshot()
        snapshots.append(snap)
        times.append(t)

        time.sleep(interval)
    
    filename = f"{DATA_DIR}/traces/trace_{now}.npz"

    snapshots = np.stack(snapshots)
    times = np.array(times)

    np.savez(filename, snapshots=snapshots, times=times)
