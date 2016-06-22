/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: nansum.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 22-Jun-2016 09:56:36
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "nansum.h"

/* Function Definitions */

/*
 * Arguments    : const double varargin_1_data[]
 *                const int varargin_1_size[1]
 * Return Type  : double
 */
double nansum(const double varargin_1_data[], const int varargin_1_size[1])
{
  double y;
  int k;
  if (varargin_1_size[0] == 0) {
    y = 0.0;
  } else {
    y = 0.0;
    for (k = 0; k + 1 <= varargin_1_size[0]; k++) {
      if (!rtIsNaN(varargin_1_data[k])) {
        y += varargin_1_data[k];
      }
    }
  }

  return y;
}

/*
 * File trailer for nansum.c
 *
 * [EOF]
 */
