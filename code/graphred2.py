mem = array()
|\CL{A:}| for i in range(A):
       mem(addr1) = ... # W1
    |\CL{B:}| for j in range(B):
           ... = mem(addr2) # R1
           ... = mem(addr3) # R2
|\CL{C:}| mem(addr3) = ... # W2
