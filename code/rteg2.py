# Input program
tmp = queue() # M1
out = queue() # M2
for i in range(N):
    for j in range(M):
        tmp.enq(i * j) # W1
for i in range(N*M):
    out.enq(tmp.deq()) # R1 and W2
...
... = out.deq() # R2

# Optimized program
out = queue() # M2
for i in range(N):
    for j in range(M):
        out.enq(i * j) # W1
...
... = out.deq() # R2
