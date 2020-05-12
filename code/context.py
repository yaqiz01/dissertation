with Context() as ctx1:
    i = Counter(min=0, max=3, stride=1)
    j = Counter(min=0, max=2, stride=1)
    chain = CounterChain(i, j);

    bufferA = VecInSteram()
    bufferB = VecInSteram()
    outputD = VecOutSteram()

    a = bufferA.deq(when=j.done())
    b = bufferB.deq(when=j.done())
    c = bufferC.deq(when=i.done())

    expr = a * b + c
    outputD.enq(data=expr, when=i.done())
