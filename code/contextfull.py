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

forward(stage=0, dst="PR0", src=c)
# b is broadcasted to all lanes
stage(0,"mul",dst="PR1", a, b)
stage(1,"add",dst="PR2",oprd=["PR0","PR1"])
forward(2,dst="PR1",src="PR1")
forward(3,dst="PR1",src="PR1")
forward(4,dst="PR1",src="PR1")
forward(5,dst="PR1",src="PR1")
outputD.enq(data="PR1", when=j.valid())
