mem = rand(N)
tmp = zeros(N)
for i in range(1, N):
    tmp[i] = mem[i-1] + i
for i in range(1, N):
    mem[i] = tmp[i]
