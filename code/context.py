with Context() as ctx:
    bufferA = VecInSteram() 
    bufferB = ScalInSteram()
    bufferC = VecInSteram()
    outputD = VecOutSteram()

    b = bufferB.deq()
    for i in range(0, 3, 1)
        c = bufferC.deq()
        for j in range(0, 3, 1)
            a = bufferA.deq()
            expr = a * b + c
            outputD.enq(data=expr)
