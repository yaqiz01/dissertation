mem = rand(N)
tmp = queue()
# Initialize queue with 
# 1 dummy element
back = queue(init=1)
@concurrent
for i in range(1, N):
    tmp.enq(mem[i-1] + i)
    back.deq()
@concurrent
for i in range(1, N):
    mem[i] = tmp.deq()
    back.enq(0)
