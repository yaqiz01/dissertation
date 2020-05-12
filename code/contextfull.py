with Context() as ctx:
    # scalar and vector input streams
    bufferA = VecInSteram() 
    bufferB = ScalInSteram()
    bufferC = VecInSteram()
    outputD = VecOutSteram()

    i = Counter(min=0,max=3,stride=1)
    j = Counter(min=0,max=3,stride=1)
    chain = CounterChain(i,j)

    a = bufferA.deq(when=j.valid())
    b = bufferB.deq(when=i.done())
    c = bufferC.deq(when=j.done())

    # b is implicitly broadcasted to all 
    # lanes
    expr = a * b + c
    outputD.enq(data=expr, when=j.valid())
