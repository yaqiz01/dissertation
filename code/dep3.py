mem = array()
|\CL{A:}| for i in range(A):
    |\CL{B:}| mem(addr1) = ... # W0
    |\CL{C:}| if cond:
        |\CL{D:}| mem(addr2) = ... # W1
       else:
        |\CL{E:}| ... = mem(addr3) # R0
|\CL{F:}| ... = mem(addr4) # R1
