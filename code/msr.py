mem = array(dims=[16])
|\CL{A:}| for i in range(16,|\CK{vec}|=16):
       data1 = ...
       mem(i) = data1 # W1
|\CL{B:}| for j in range(M):
    |\CL{C:}| for i in range(16,|\CK{vec}|=16):
           data2 = mem(15-i) # R1
           ...
