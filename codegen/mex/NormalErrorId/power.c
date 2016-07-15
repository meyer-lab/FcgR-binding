/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * power.c
 *
 * Code generation for function 'power'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorId.h"
#include "power.h"
#include "scalexpAlloc.h"

/* Variable Definitions */
static emlrtRSInfo j_emlrtRSI = { 49, "power",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\power.m" };

static emlrtRSInfo k_emlrtRSI = { 58, "power",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\power.m" };

static emlrtRSInfo l_emlrtRSI = { 73, "applyScalarFunction",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\applyScalarFunction.m"
};

static emlrtRTEInfo d_emlrtRTEI = { 17, 19, "scalexpAlloc",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\scalexpAlloc.m"
};

/* Function Definitions */
void power(const emlrtStack *sp, real_T a, const real_T b_data[], const int32_T
           b_size[2], real_T y_data[], int32_T y_size[2])
{
  int32_T k;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &j_emlrtRSI;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  b_st.site = &k_emlrtRSI;
  c_st.site = &l_emlrtRSI;
  y_size[0] = 1;
  y_size[1] = (int8_T)b_size[1];
  if (dimagree(y_size, b_size)) {
  } else {
    emlrtErrorWithMessageIdR2012b(&c_st, &d_emlrtRTEI, "MATLAB:dimagree", 0);
  }

  for (k = 0; k + 1 <= b_size[1]; k++) {
    y_data[k] = muDoubleScalarPower(a, b_data[k]);
  }
}

/* End of code generation (power.c) */
