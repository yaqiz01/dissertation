# Input program
accum = 0 # M1
out = 0 # M2
for i in range(N):
    for j in range(M):
        accum += i * j # W1
    out = accum # R1 and W2
...
... = out # R2

# Optimized program
out = 0 # M2
for i in range(N):
    for j in range(M):
        out += i * j # W1
...
... = out # R2
