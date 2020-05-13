mem = OnchipArray(dims=[100])
|\CL{A:}| for i in range(A,|\CK{par}|=2):
    ## A0: lane 0 of unrolled loop A
    |\CL{B:}| for j in range(B):
        mem(addr1) = data1 # W0
    |\CL{C:}| for k in range(C):
        data2 = mem(addr2) # R0
    ## A1: lane 1 of unrolled loop A
    |\CL{B:}| for j in range(B):
        mem(addr1) = data1 # W1
    |\CL{C:}| for k in range(C):
        data2 = mem(addr2) # R1
