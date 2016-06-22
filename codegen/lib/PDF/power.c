/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: power.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 22-Jun-2016 09:56:36
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "power.h"
#include "PDF_emxutil.h"
#include "PDF_rtwutil.h"

/* Function Definitions */

/*
 * Arguments    : const double b[24]
 *                double y[24]
 * Return Type  : void
 */
void b_power(const double b[24], double y[24])
{
  int k;
  for (k = 0; k < 24; k++) {
    y[k] = rt_powd_snf(10.0, b[k]);
  }
}

/*
 * Arguments    : double a
 *                const emxArray_real_T *b
 *                emxArray_real_T *y
 * Return Type  : void
 */
void c_power(double a, const emxArray_real_T *b, emxArray_real_T *y)
{
  unsigned int b_idx_0;
  int k;
  b_idx_0 = (unsigned int)b->size[0];
  k = y->size[0];
  y->size[0] = (int)b_idx_0;
  emxEnsureCapacity((emxArray__common *)y, k, (int)sizeof(double));
  for (k = 0; k + 1 <= b->size[0]; k++) {
    y->data[k] = rt_powd_snf(a, b->data[k]);
  }
}

/*
 * Arguments    : double a
 *                const emxArray_real_T *b
 *                emxArray_real_T *y
 * Return Type  : void
 */
void d_power(double a, const emxArray_real_T *b, emxArray_real_T *y)
{
  int k;
  k = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = b->size[1];
  emxEnsureCapacity((emxArray__common *)y, k, (int)sizeof(double));
  for (k = 0; k + 1 <= b->size[1]; k++) {
    y->data[k] = rt_powd_snf(a, b->data[k]);
  }
}

/*
 * Arguments    : const double b[7]
 *                double y[7]
 * Return Type  : void
 */
void power(const double b[7], double y[7])
{
  int k;
  for (k = 0; k < 7; k++) {
    y[k] = rt_powd_snf(10.0, b[k]);
  }
}

/*
 * File trailer for power.c
 *
 * [EOF]
 */
