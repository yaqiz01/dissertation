mem = VirtualMemory(dims=[100])

with Context() as ctxB:
    |\CL{A:}| for i in range(A):
        |\CL{B:}| for j in range(B):
            addr1, data1 = ...
            mem(addr1) = data1 # W1

with Context() as ctxC:
    |\CL{A:}| for i in range(A):
        |\CL{C:}| for k in range(C):
            addr2 = ...
            data2 = mem(addr2) # R1
            ...
