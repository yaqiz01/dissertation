// Host to accelerator register for scalar input with 
// user annotated value
val N = ArgIn[Int]; 
bound(N) = 1024
// 1-D DRAM size in N
val vecA, vecB = DRAM[T](N)
// 2-D DRAM size in NxN
val matC = DRAM[T](N, N)
// Loop unrolling factors
val op1, op2, ip:Int = ...
// Blocking sizes of vecA and vecB
val tsA, tsB:Int = ...

// Accelerator kernel
Accel {
  // Parallelized by op1
  Foreach(min=0, step=tsA, max=N, par=op1){ i =>
    // Allocate 1-D scratchpad size in tsA
    val tileA = SRAM[T](tsA)
    // Load range i to i+tsA of vectorA from off- to 
    // on-chip parallelized by ip
    tileA load vecA(i::i+tsA par ip) 
    Foreach(min=0, step=tsB, max=N, par=op2) { j =>
      val tileB = SRAM[T](tsB)
      tileB load vecB(j::j+tsB par ip) 
      // 2-D scratchpad
      val tileC = SRAM[T](tsA, tsB)
      Foreach(min=0, step=1, max=tsA){ ii =>
        Foreach(min=0, step=1, max=tsB, par=ip) { jj =>
          tileC(ii, jj) = tileA(ii) * tileB(jj)
        }
      }
      // Store partial results to DRAM
      matC(i::i+tsA, j::j+tsB par ip) store tileC
    }
  }
}

