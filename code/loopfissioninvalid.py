for i in range(1, N):
    mem[i] = mem[i-1] + i

tmp = zeros_like(mem)
for i in range(1, N):
    tmp[i] = mem[i-1] + i
for i in range(1, N):
    mem[i] = tmp[i]


tmp = queue()
back = queue()
back.push(0)

for i in range(1, N):
    tmp.enq(mem[i-1] + i)
    back.deq()

for i in range(1, N):
    mem[i] = tmp.deq()
    back.enq(0)
