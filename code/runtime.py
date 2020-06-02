# A stream from the network
stream = queue()
...
# User annotaiton on the number of packets from stream
count[stream] = N

# Forever loop
@streaming
|\CL{A:}| for i in range(*):
    mem = array(dims=[100])
    q = queue()
    |\CL{B:}| for j in range(B):
        mem(j) = stream.deq() # W1
        q.enq(k) # W2
    |\CL{C:}| for k in range(C):
        cond = k % 2 == 0
        # User annotaiton on fraction of the time cond evaluates to true
        true_ratio[cond] = R
        |\CL{D:}| if cond:
            |\CL{E:}| for m in range(E):
                   ... = mem(m) # R1
                   ... = q.deq() # R2
