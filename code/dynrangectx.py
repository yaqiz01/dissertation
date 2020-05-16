bound = ScalarStream()
with Context() as ctx1:
    |\CL{A:}| for i in range(N):
        bound.enq(2*i)
with Context() as ctx2:
    |\CL{A:}| for i in range(N):
        start = bound.deq()
        |\CL{B:}| for j in range(start, N):
            ... = i + j
