/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * nansum.c
 *
 * Code generation for function 'nansum'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "nansum.h"
#include "PDF_data.h"

/* Variable Definitions */
static emlrtBCInfo j_emlrtBCI = { -1, -1, 75, 19, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtRTEInfo f_emlrtRTEI = { 30, 27, "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m"
};

static emlrtRTEInfo g_emlrtRTEI = { 27, 27, "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m"
};

static emlrtBCInfo k_emlrtBCI = { -1, -1, 76, 21, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

/* Function Definitions */
real_T b_nansum(const real_T varargin_1[8])
{
  real_T y;
  int32_T k;
  y = 0.0;
  for (k = 0; k < 8; k++) {
    if (!muDoubleScalarIsNaN(varargin_1[k])) {
      y += varargin_1[k];
    }
  }

  return y;
}

real_T nansum(const emlrtStack *sp, const real_T varargin_1_data[], const
              int32_T varargin_1_size[1])
{
  real_T y;
  boolean_T p;
  boolean_T b_p;
  int32_T k;
  int32_T exitg1;
  int32_T b_k;
  emlrtStack st;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &p_emlrtRSI;
  p = false;
  b_p = false;
  k = 0;
  do {
    exitg1 = 0;
    if (k < 2) {
      if (k + 1 <= 1) {
        b_k = varargin_1_size[0];
      } else {
        b_k = 1;
      }

      if (b_k != 0) {
        exitg1 = 1;
      } else {
        k++;
      }
    } else {
      b_p = true;
      exitg1 = 1;
    }
  } while (exitg1 == 0);

  if (!b_p) {
  } else {
    p = true;
  }

  if (!p) {
  } else {
    emlrtErrorWithMessageIdR2012b(&st, &g_emlrtRTEI,
      "Coder:toolbox:sum_specialEmpty", 0);
  }

  if ((varargin_1_size[0] == 1) || (varargin_1_size[0] != 1)) {
    p = true;
  } else {
    p = false;
  }

  if (p) {
  } else {
    emlrtErrorWithMessageIdR2012b(&st, &f_emlrtRTEI,
      "Coder:toolbox:autoDimIncompatibility", 0);
  }

  if (varargin_1_size[0] == 0) {
    y = 0.0;
  } else {
    y = 0.0;
    for (k = 1; k <= varargin_1_size[0]; k++) {
      if (!((k >= 1) && (k <= varargin_1_size[0]))) {
        emlrtDynamicBoundsCheckR2012b(k, 1, varargin_1_size[0], &j_emlrtBCI, &st);
      }

      if (!muDoubleScalarIsNaN(varargin_1_data[k - 1])) {
        if (!((k >= 1) && (k <= varargin_1_size[0]))) {
          emlrtDynamicBoundsCheckR2012b(k, 1, varargin_1_size[0], &k_emlrtBCI,
            &st);
        }

        y += varargin_1_data[k - 1];
      }
    }
  }

  return y;
}

/* End of code generation (nansum.c) */
