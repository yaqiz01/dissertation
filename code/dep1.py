mem = array()
|\CL{A:}| for i in range(A,|\CK{par}|=2):
    |\CL{B:}| for j in range(B):
           mem(addr1) = data1 # W
    |\CL{C:}| for k in range(C):
           data2 = mem(addr2) # R
