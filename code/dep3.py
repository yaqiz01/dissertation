mem = OnchipArray(dims=[100])
|\CL{A:}| for i in range(A):
      mem(addr1) = ... # W1
   |\CL{B:}| if cond:
      |\CL{C:}| mem(addr2) = ... # W2
      else:
      |\CL{D:}| ... mem(add3) # R1
