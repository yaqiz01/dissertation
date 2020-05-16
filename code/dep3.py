mem = OnchipArray(dims=[100])
|\CL{A:}| for i in range(A):
    |\CL{B:}| mem(addr1) = ... # W1
    |\CL{C:}| if cond:
        |\CL{D:}| mem(addr2) = ... # W2
       else:
        |\CL{E:}| ... mem(add3) # R1
