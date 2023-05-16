import sys

filename = sys.argv[1]

line_number = 1
with open(filename, "r") as file:
    entry_time = ""
    for line in file:
        line_number += 1
        line = line.strip()
        # print(line_number)
        if "entry" in line:
            entry_time = line.split()[2].split(":")[0]
        if "exit" in line:
            if "vector" in line:
                irq_number = line.split("vector=")[1].split()[0]
            else:
                irq_number = line.split("irq=")[1].split()[0]
            exit_time = line.split()[2].split(":")[0]
            event = line.split()[3].rstrip(":")
            print("IRQ: {}, Entry: {}, Exit: {}".format(irq_number, entry_time, exit_time))