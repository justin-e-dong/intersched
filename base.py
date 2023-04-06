import json
import sys
import os
import time
from datetime import datetime
import numpy as np
import ctypes

# redis_01: redis-benchmark -t get -n 1000000 -d 8 -c 100
# redis_02: redis-benchmark -t set -n 1000000 -d 8 -c 100

# postgres_01: pgbench -c 100 -j 100 -t 10000 testdb
# postgres_02: pgbench -c 100 -j 100 -t 100000 -S testdb
# postgres_03: pgbench -c 100 -j 100 -t 10000 -N testdb

# postgres_06: pgbench -h localhost -p 5432 -U justin -c 100 -j 100 -T 100 testdb -f sql/random_parallel_writes.sql

DATA_DIR = "postgres_12"
TRACE_DIR = "traces"

CLOCK_REALTIME = 0

class timespec(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_int64), # seconds, https://stackoverflow.com/q/471248/1672565
        ('tv_nsec', ctypes.c_int64), # nanoseconds
        ]

clock_gettime = ctypes.cdll.LoadLibrary('libc.so.6').clock_gettime
clock_gettime.argtypes = [ctypes.c_int64, ctypes.POINTER(timespec)]
clock_gettime.restype = ctypes.c_int64    

def time_ns():
    tmp = timespec()
    ret = clock_gettime(CLOCK_REALTIME, ctypes.pointer(tmp))
    if bool(ret):
        raise OSError()
    return tmp.tv_sec * 10 ** 9 + tmp.tv_nsec

def get_snapshot():
    full_data = None
    now = time_ns()
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

    return np.array(res), now

# interval in seconds
def collect_and_dump_trace(interval=0.5, count=100):
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
