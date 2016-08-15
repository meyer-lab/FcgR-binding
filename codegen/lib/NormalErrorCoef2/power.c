/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: power.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 15-Aug-2016 17:19:22
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef2.h"
#include "power.h"
#include "NormalErrorCoef2_rtwutil.h"

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
  double x;
  int loop_ub;
  int i0;
  double b_y_data[30];
  int k;
  int b_k;
  x = a;
  loop_ub = b_size[0] * b_size[1];
  for (i0 = 0; i0 < loop_ub; i0++) {
    b_y_data[i0] = b_data[i0];
  }

  y_size[0] = 1;
  y_size[1] = (signed char)b_size[1];
  loop_ub = b_size[1];

#pragma omp parallel for \
 num_threads(omp_get_max_threads()) \
 private(b_k)

  for (k = 1; k <= loop_ub; k++) {
    b_k = k;
    y_data[b_k - 1] = rt_powd_snf(x, b_y_data[b_k - 1]);
  }
}

/*
 * File trailer for power.c
 *
 * [EOF]
 */
