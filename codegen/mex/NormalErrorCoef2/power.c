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
#include "NormalErrorCoef2.h"
#include "power.h"
#include "scalexpAlloc.h"

/* Variable Definitions */
static emlrtRSInfo o_emlrtRSI = { 49, "power",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\ops\\power.m" };

static emlrtRSInfo p_emlrtRSI = { 58, "power",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\ops\\power.m" };

static emlrtRSInfo q_emlrtRSI = { 73, "applyScalarFunction",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\eml\\+coder\\+internal\\applyScalarFunction.m"
};

static emlrtRTEInfo d_emlrtRTEI = { 17, 19, "scalexpAlloc",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\eml\\+coder\\+internal\\scalexpAlloc.m"
};

/* Function Definitions */
void power(const emlrtStack *sp, real_T a, const real_T b_data[], const int32_T
           b_size[2], real_T y_data[], int32_T y_size[2])
{
  real_T x;
  int32_T loop_ub;
  int32_T i0;
  real_T b_y_data[30];
  int32_T k;
  int32_T b_k;
  jmp_buf * volatile emlrtJBStack;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &o_emlrtRSI;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  b_st.site = &p_emlrtRSI;
  x = a;
  loop_ub = b_size[0] * b_size[1];
  for (i0 = 0; i0 < loop_ub; i0++) {
    b_y_data[i0] = b_data[i0];
  }

  c_st.site = &q_emlrtRSI;
  y_size[0] = 1;
  y_size[1] = (int8_T)b_size[1];
  if (dimagree(y_size, b_size)) {
  } else {
    emlrtErrorWithMessageIdR2012b(&c_st, &d_emlrtRTEI, "MATLAB:dimagree", 0);
  }

  loop_ub = b_size[1];
  emlrtEnterParallelRegion(&b_st, omp_in_parallel());
  emlrtPushJmpBuf(&b_st, &emlrtJBStack);

#pragma omp parallel for \
 num_threads(emlrtAllocRegionTLSs(b_st.tls, omp_in_parallel(), omp_get_max_threads(), omp_get_num_procs())) \
 private(b_k)

  for (k = 1; k <= loop_ub; k++) {
    b_k = k;
    y_data[b_k - 1] = muDoubleScalarPower(x, b_y_data[b_k - 1]);
  }

  emlrtPopJmpBuf(&b_st, &emlrtJBStack);
  emlrtExitParallelRegion(&b_st, omp_in_parallel());
}

/* End of code generation (power.c) */
