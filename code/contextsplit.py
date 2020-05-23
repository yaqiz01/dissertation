mem = VirtualMemory(dims=[100])
token = ControlStream()
credit = ControlStream(init=2)

with Context() as ctxB:
    |\CL{A:}| for i in range(A):
        credit.deq()
        |\CL{B:}| for j in range(B):
            waddr, wdata = ...
            mem.waddr.enq(waddr)
            mem.wdata.enq(wdata)
with Context() as respW1:
    |\CL{A:}| for i in range(A):
        |\CL{B:}| for j in range(B):
            ack1 = mem.ack.deq()
        token.enq()

with Context() as rqstR1:
    |\CL{A:}| for i in range(A):
        token.deq()
        |\CL{C:}| for k in range(C):
            raddr = ...
            mem.raddr.enq(raddr)
with Context() as ctxC:
    |\CL{A:}| for i in range(A):
        |\CL{C:}| for k in range(C):
            rdata = mem.rdata.deq()
            ...
        credit.enq()
