import numpy as np

full_data = None
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

print(len(col_labels))
print(len(row_labels))

print(len(res))
