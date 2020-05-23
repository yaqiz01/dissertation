mem = VirtualMemory(dims=[100])

wstream = VecSteram()
with Context() as ctxB:
    |\CL{A:}| for i in range(A):
        |\CL{B:}| for j in range(B):
            wdata = ...
            wstream.enq(wdata)

with VirtualUnit() as vu:
    token = ControlStream()
    credit = ControlStream(init=2)
    with Context() as rqstW1:
        |\CL{A:}| for i in range(A):
            credit.deq()
            |\CL{B:}| for j in range(B):
                waddr = ...
                mem.waddr.enq(waddr)
                mem.wdata.enq(wdata)
            token.enq()
    with Context() as rqstR1:
        |\CL{A:}| for i in range(A):
            token.deq()
            |\CL{C:}| for k in range(C):
                raddr = ...
                mem.raddr.enq(raddr)
            credit.enq()

with Context() as ctxC:
    |\CL{A:}| for i in range(A):
        |\CL{C:}| for k in range(C):
            rdata = mem.rdata.deq()
            ...
