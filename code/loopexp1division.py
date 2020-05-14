mem = zeros(N)
a = rand(N)
b = rand(N)
tmp = queue()
@concurrent
for i in range(1, N):
    tmp.enq(a[i] * b[i])
@concurrent
for i in range(1, N):
    mem[i] = tmp.deq() + i
