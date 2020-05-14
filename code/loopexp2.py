mem = rand(N)
for i in range(1, N):
    tmp = mem[i-1] + i
    mem[i] = tmp
