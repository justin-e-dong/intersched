import sys

input_file = sys.argv[1] + ".log"
output_file = sys.argv[1] + ".parsed"

def clean_traces(input_file, output_file):
    data = []
    line_number = 0
    start_time = 0
    unique_irqs = set()
    num_irqs = 0
    num_interrupts = 0
    output_string = ""
    with open(input_file, "r") as file:
        entry_time = ""
        for line in file:
            line_number += 1
            line = line.strip()
            # print(line_number)

            if line_number == 2:
                start_time = float(line.split()[2].split(":")[0]) * 1e9

            if "entry" in line:
                entry_time = float(line.split()[2].split(":")[0]) * 1e9 - start_time
            if "exit" in line:
                if "vector" in line:
                    irq_number = line.split("vector=")[1].split()[0]
                else:
                    irq_number = line.split("irq=")[1].split()[0]
                exit_time = float(line.split()[2].split(":")[0]) * 1e9 - start_time
                interrupt_length = exit_time - entry_time
                event = line.split()[3].rstrip(":")
                curr_string = "IRQ: {}, Entry: {}, Length: {}".format(irq_number, entry_time, interrupt_length)
                data.append(curr_string)
                output_string += curr_string + "\n"
                unique_irqs.add(irq_number)
    unique_irqs = list(unique_irqs)
    num_irqs = len(unique_irqs)
    num_interrupts = len(data)

    with open(output_file, 'w') as file_write:
                    file_write.write(output_string + "\n")

    return num_irqs, unique_irqs, num_interrupts, data


clean_traces(input_file, output_file)