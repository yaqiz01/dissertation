mem = zeros(N)
a = rand(N)
b = rand(N)
for i in range(1, N):
    tmp = a[i] * b[i]
    mem[i] = tmp + i
