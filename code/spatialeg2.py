mem = array(dims=[100])
|\CL{A:}| for i in range(A,|\CK{par}|=m):
    |\CL{B:}| for j in range(B,|\CK{vec}|=n):
        # a basic block with x 
        # operations
        waddr, wdata = ...
        mem(waddr) = wdata # W1
        ...
    |\CL{C:}| for k in range(C,|\CK{vec}|=n):
        # a basic block with y 
        # operations
        raddr = ...
        rdata = mem(raddr) # R1
        ...

