from base import collect_and_dump_trace

max_iters = 10
for i in range(max_iters):
    print("Count " + str(i * 10) + "/" + str(max_iters * 10))
    collect_and_dump_trace(interval=0.1, count=10)