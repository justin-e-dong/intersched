## Interrupt Traces

This is only for coarse-grained interrupt collection. We do not know precisely when interrupts happen, you need to collect that sort of data at the kernel level

Important note: need to consider that the Python script you are running to collect the data impacts the interrupt counts. Collecting data at kernel level probably would not have as great of an impact

## TODO

- Create cron job to collect at 1s intervals
- Save the table data for `/proc/interrupts` at 1s intervals

## Git Note

For using the SSH key I want to push to GitHub from the 4socket server:

```git config --add --local core.sshCommand 'ssh -i ~/.ssh/int_traces'```

## Numbers

During LLVM build, per-CPU interrupt rate of: `120.05`
