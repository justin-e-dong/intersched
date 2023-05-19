def clean_data(filename):
    data = []
    line_number = 0
    start_time = 0
    with open(filename, "r") as file:
        entry_time = ""
        for line in file:
            line_number += 1
            line = line.strip()
            # print(line_number)

            if line_number == 2:
                start_time = float(line.split()[2].split(":")[0])

            if "entry" in line:
                entry_time = float(line.split()[2].split(":")[0]) - start_time
            if "exit" in line:
                if "vector" in line:
                    irq_number = line.split("vector=")[1].split()[0]
                else:
                    irq_number = line.split("irq=")[1].split()[0]
                exit_time = float(line.split()[2].split(":")[0]) - start_time
                event = line.split()[3].rstrip(":")
                data.append("IRQ: {}, Entry: {}, Exit: {}".format(irq_number, entry_time, exit_time))

    return data