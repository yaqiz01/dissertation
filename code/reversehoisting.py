mem1 = rand(N)
mem2 = rand(N)
for i in range(N):
    # Block 2
    c = a + b
    mem2[i] += mem[i] * c
