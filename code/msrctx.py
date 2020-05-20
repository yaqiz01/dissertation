mem = VectorStream()
with Context() as ctxA:
    # Loop A is optimized away
    data1 = ...
    mem.enq(data1)
with Context() as ctxC:
    ## vector constants
    fromAddr = xrange(0,16)
    toAddr = xrange(start=15,end=-1,step=-1)
    |\CL{B:}| for j in range(M):
           # Loop C is optimized away
           tmp = mem.deq()
           data2 = shuffle(from=fromAddr,
                   to=toAddr,base=tmp)
           ...
