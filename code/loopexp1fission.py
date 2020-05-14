mem = zeros(N)
a = rand(N)
b = rand(N)
tmp = zeros(N)
for i in range(1, N):
    tmp[i] = a[i] * b[i]
for i in range(1, N):
    mem[i] = tmp[i] + i
