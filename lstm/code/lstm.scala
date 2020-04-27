// Number of hidden units in h and features in x
val H, D = ...
// Loop unrolling / vectorization parameters
val hu, ru, hv, rv = ...
val c = SRAM[T](H) // SRAM storing C
val xh = SRAM[T](D+H) // SRAM storing [X,H]
// Concatenated weights [Wx,Wh] for each gate in 2-D SRAMs
val wi, wj, wf, wo:SRAM2[T] = ...
val bi, bj, bf, bo: SRAM[T] = ... // Bias
// Lookup tables for non-linear functions
val luti, lutj, luf, luto: SRAM[T] = ...
val tanh:SRAM[T] = ... // Lookup table for tanh
Sequential.Foreach (nSteps by 1){ step =>
  // Loop range from 0 to H parallelized by hu
  Foreach(H par hu){ ih =>
    def fusedDotProductWithNonLinear(w:SRAM2[T], lut:SRAM[T], b:SRAM[T]) = {
      // Tiled dot product with blocking size of rv parallelized by ru
      val elem = Reduce(Reg[T])((D+H) by rv par ru){ iu =>
        Reduce(Reg[T])(rv par rv){ iv =>
          val iuv = iu + iv
          w(ih, iuv) * xh(iuv)
        }{ (a,b) => a + b }
      }{ (a,b) => a + b }.value + b(ih)
      lut(elem)
    }
    val i = fusedDotProductWithNonLinear(wi, luti, bi)
    val j = fusedDotProductWithNonLinear(wj, lutj, bj)
    val f = fusedDotProductWithNonLinear(wf, lutf, bf)
    val o = fusedDotProductWithNonLinear(wo, luto, bo)
    val cNew = i*j + c(ih) * f
    c(ih) = cNew
    xh(ih+D) = tanh(cNew) * o
  }
}
