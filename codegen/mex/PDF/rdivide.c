/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * rdivide.c
 *
 * Code generation for function 'rdivide'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "rdivide.h"

/* Function Definitions */
void rdivide(const real_T x[24], const real_T y[24], real_T z[24])
{
  int32_T i2;
  for (i2 = 0; i2 < 24; i2++) {
    z[i2] = x[i2] / y[i2];
  }
}

/* End of code generation (rdivide.c) */
