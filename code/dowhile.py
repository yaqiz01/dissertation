# This is an approximation of the 
# do while loop in python syntax
accum = 0
# A loop running forver until stop 
# is True
stop = False
|\CL{A:}| for i in range(*) |\CK{until}| stop:
    |\CL{B:}| for j in range(N):
           accum += i
    |\CL{C:}| stop = i > 100
|\CL{D:}| ... = accum
