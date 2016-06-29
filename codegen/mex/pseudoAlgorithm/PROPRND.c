/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PROPRND.c
 *
 * Code generation for function 'PROPRND'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "PROPRND.h"
#include "pseudoAlgorithm_data.h"

/* Function Definitions */
void PROPRND(const emlrtStack *sp, const real_T current[11], real_T next[11])
{
  real_T r[9];
  int32_T i4;
  real_T b_r;
  memset(&next[0], 0, 11U * sizeof(real_T));
  emlrtRandn(r, 9);
  for (i4 = 0; i4 < 9; i4++) {
    r[i4] *= 0.039;
  }

  for (i4 = 0; i4 < 9; i4++) {
    next[i4] = current[i4] + r[i4];
  }

  while ((next[9] < 1.0) || (4.0 < next[9])) {
    emlrtRandu(&b_r, 1);
    next[9] = (current[9] + (1.0 + muDoubleScalarFloor(b_r * 3.0))) - 2.0;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  while ((next[10] < 1.0) || (26.0 < next[10])) {
    emlrtRandu(&b_r, 1);
    next[10] = (current[10] + (1.0 + muDoubleScalarFloor(b_r * 3.0))) - 2.0;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }
}

/* End of code generation (PROPRND.c) */
