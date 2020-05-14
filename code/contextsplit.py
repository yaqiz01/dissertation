mem = VirtualMemory(dims=[100])
token = ControlStream()
credit = ControlStream(init=1)

with Context() as ctxB:
    |\CL{A:}| for i in range(A):
        |\CL{B:}| for j in range(B):
            addr1, data1 = ...
            mem.addr.enq(addr1)
            mem.data.enq(data1)
        credit.deq()
with Context() as respW1:
    |\CL{A:}| for i in range(A):
        |\CL{B:}| for j in range(B):
            ack1 = mem.ack.deq()
        token.enq()

with Context() as rqstR1:
    |\CL{A:}| for i in range(A):
        |\CL{C:}| for k in range(C):
            addr2 = ...
            mem.reqst.enq(addr2)
        token.deq()
with Context() as ctxC:
    |\CL{A:}| for i in range(A):
        |\CL{C:}| for k in range(C):
            data2 = mem.resp.deq()
            ...
        credit.enq()
