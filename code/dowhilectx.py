
# These streams are initialized with 
# one initial element.
stop = ScalarStream(init=False)
accum2 = ScalarStream()
with Context() as ctxB:
    accum1 = AccumPR(init=0)
    |\CL{A:}| for i in range(*):
        cond = stop.deq()
        if cond: break
        |\CL{B:}| for j in range(N):
               accum1.accum(i)
    accum2.enq(accum1.value())
    accum1.reset()

with Context() as ctxC:
    |\CL{A:}| for i in range(*):
        cond = stop.deq()
        if cond: break
        |\CL{C:}| stop.enq(i > 100)

with Context() as ctxD:
    |\CL{D:}| ... = accum2.deq()
