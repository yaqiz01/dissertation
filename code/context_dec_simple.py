bufferA = VecSteram() 
bufferB = ScalarStream()
bufferC = VecSteram()
outputD = VecSteram()

with Context() as ctx:
    b = bufferB.deq()
    i = Counter(0,3,1)
    j = Counter(0,3,1)
    ctx.chain(i,j)
    b = bufferB.deq(when=i.done())
    c = bufferC.deq(when=j.done())
    a = bufferA.deq(when=j.valid())

    expr = a * b + c
    outputD.enq(data=expr, when=j.valid())
