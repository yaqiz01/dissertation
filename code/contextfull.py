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
stage(0,"mul",dst="PR1", b, c)
# Operands are PRs from the previous stage
stage(1,"add",dst="PR2",oprd=["PR0","PR1"])

# forwarding PR2 of stage 1 to stage 2
forward(stage=2,dst="PR2",src="PR2")
forward(stage=3,dst="PR2",src="PR2")
forward(stage=4,dst="PR2",src="PR2")
forward(stage=5,dst="PR2",src="PR2")
forward(stage=0,dst="PR3",src=j.valid())
forward(stage=1,dst="PR3",src="PR3")
forward(stage=2,dst="PR3",src="PR3")
forward(stage=3,dst="PR3",src="PR3")
forward(stage=4,dst="PR3",src="PR3")
forward(stage=5,dst="PR3",src="PR3")
outputD.enq(data="PR2", when="PR3")
