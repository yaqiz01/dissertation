mem1 = rand(N)
mem2 = rand(N)
# Block 1
c = a + b
for i in range(N):
    # Block 2
    mem2[i] += mem[i] * c
