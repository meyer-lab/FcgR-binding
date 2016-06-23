/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: power.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 23-Jun-2016 16:03:51
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "power.h"
#include "PDF_rtwutil.h"

/* Function Definitions */

/*
 * Arguments    : double a
 *                const double b_data[]
 *                const int b_size[2]
 *                double y_data[]
 *                int y_size[2]
 * Return Type  : void
 */
void power(double a, const double b_data[], const int b_size[2], double y_data[],
           int y_size[2])
{
  int k;
  y_size[0] = 1;
  y_size[1] = (signed char)b_size[1];
  for (k = 0; k + 1 <= b_size[1]; k++) {
    y_data[k] = rt_powd_snf(a, b_data[k]);
  }
}

/*
 * File trailer for power.c
 *
 * [EOF]
 */
