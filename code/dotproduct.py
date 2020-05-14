with Context() as ctx:
    bufferA = VecInSteram() 
    bufferB = VecInStream()
    bufferN = ScalInStream()
    bufferAcc = ScalOutStream()

    for i in range(0, N, 16)
        a = bufferA.deq()
        b = bufferA.deq()
        # vectorized multiply
        prod = a * b
        # produce a scalar ouptut
        r = reduce(prod, lambda a,b: a+b)
        # scalar accumlation in PR
        accum += r
    # sends bufferAcc every N/16 cycles
    bufferAcc.enq(accum)
