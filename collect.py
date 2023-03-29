from base import collect_and_dump_trace

max_iters = 1
for i in range(max_iters):
    print("Count " + str(i * 20) + "/" + str(max_iters * 50))
    collect_and_dump_trace(count=20)