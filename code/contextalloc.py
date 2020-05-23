mem = VirtualMemory(dims=[100])

with Context() as ctxB:
    |\CL{A:}| for i in range(A):
        |\CL{B:}| for j in range(B):
            waddr, wdata = ...
            mem(waddr) = wdata # W1

with Context() as ctxC:
    |\CL{A:}| for i in range(A):
        |\CL{C:}| for k in range(C):
            raddr = ...
            rdata = mem(raddr) # R1
            ...
