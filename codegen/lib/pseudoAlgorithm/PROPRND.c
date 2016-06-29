/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PROPRND.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "PROPRND.h"
#include "rand.h"
#include "randn.h"

/* Function Definitions */

/*
 * Arguments    : const double current[11]
 *                double next[11]
 * Return Type  : void
 */
void PROPRND(const double current[11], double next[11])
{
  double r[9];
  int i6;
  double b_r;
  memset(&next[0], 0, 11U * sizeof(double));
  randn(r);
  for (i6 = 0; i6 < 9; i6++) {
    next[i6] = current[i6] + r[i6] * 0.039;
  }

  while ((next[9] < 1.0) || (4.0 < next[9])) {
    b_r = f_rand();
    next[9] = (current[9] + (1.0 + floor(b_r * 3.0))) - 2.0;
  }

  while ((next[10] < 1.0) || (26.0 < next[10])) {
    b_r = f_rand();
    next[10] = (current[10] + (1.0 + floor(b_r * 3.0))) - 2.0;
  }
}

/*
 * File trailer for PROPRND.c
 *
 * [EOF]
 */
