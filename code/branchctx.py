even = ScalarStream()
odd = ScalarStream()
token = ControlStream()
credit = ControlStream(init=2)
with Context() as ctxB:
 |\CL{A:}| for i in range(A):
     |\CL{B:}| tmp = i % 2 == 0
        even.enq(tmp)
        odd.enq(not tmp)
with Context() as ctxD:
 |\CL{A:}| for i in range(A):
     |\CL{C:}| if even.deq():
         |\CL{D:}| for j in range(D):
                addr1, data1 = ...
                mem.waddr.enq(data1)
                mem.wdata.enq(data1)
        credit.deq()
with Context() as rpstW:
 |\CL{A:}| for i in range(A):
     |\CL{C:}| if even.deq():
         |\CL{D:}| for j in range(D):
             mem.wack.deq()
        token.enq()
with Context() as rqstR:
 |\CL{A:}| for i in range(A):
     |\CL{C:}| if odd.deq():
         |\CL{F:}| for k in range(F):
             addr2 = ...
             mem.raddr.deq(addr2)
        token.deq()
with Context() as ctxF:
 |\CL{A:}| for i in range(A):
     |\CL{C:}| if odd.deq():
         |\CL{F:}| for k in range(F):
             data2 = mem.rdata.deq()
             ...
        credit.enq()
