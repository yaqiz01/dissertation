|\CL{A:}| for i in range(A):
    |\CL{B:}| even = i % 2 == 0
    |\CL{C:}| if even:
        |\CL{D:}| for j in range(D):
            addr1, data1 = ...
            mem(addr1) = data1 # W
       else:
        |\CL{F:}| for k in range(F):
            addr2 = ...
            data2 = mem(addr2) # R
            ...
