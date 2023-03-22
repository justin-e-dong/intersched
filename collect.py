from base import collect_and_dump_trace

max_iters = 100
for i in range(max_iters):
    print("Count " + str(i * 100) + "/" + str(max_iters * 100))
    collect_and_dump_trace(count=100)