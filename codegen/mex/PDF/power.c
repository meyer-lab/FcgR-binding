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
#include "PDF.h"
#include "power.h"
#include "eml_int_forloop_overflow_check.h"
#include "PDF_emxutil.h"
#include "scalexpAlloc.h"

/* Variable Definitions */
static emlrtRSInfo k_emlrtRSI = { 20, "eml_int_forloop_overflow_check",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\eml\\eml_int_forloop_overflow_check.m"
};

static emlrtRSInfo l_emlrtRSI = { 49, "power",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\power.m" };

static emlrtRSInfo m_emlrtRSI = { 58, "power",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\power.m" };

static emlrtRSInfo n_emlrtRSI = { 73, "applyScalarFunction",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\applyScalarFunction.m"
};

static emlrtRSInfo o_emlrtRSI = { 101, "applyScalarFunction",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\applyScalarFunction.m"
};

static emlrtRTEInfo b_emlrtRTEI = { 16, 9, "scalexpAlloc",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\scalexpAlloc.m"
};

static emlrtRTEInfo e_emlrtRTEI = { 17, 19, "scalexpAlloc",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\scalexpAlloc.m"
};

/* Function Definitions */
void b_power(const real_T b[24], real_T y[24])
{
  int32_T k;
  for (k = 0; k < 24; k++) {
    y[k] = muDoubleScalarPower(10.0, b[k]);
  }
}

void c_power(const emlrtStack *sp, real_T a, const emxArray_real_T *b,
             emxArray_real_T *y)
{
  uint32_T b_idx_0;
  int32_T k;
  boolean_T overflow;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &l_emlrtRSI;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  b_st.site = &m_emlrtRSI;
  c_st.site = &n_emlrtRSI;
  b_idx_0 = (uint32_T)b->size[0];
  k = y->size[0];
  y->size[0] = (int32_T)b_idx_0;
  emxEnsureCapacity(&c_st, (emxArray__common *)y, k, (int32_T)sizeof(real_T),
                    &b_emlrtRTEI);
  if (dimagree(y, b)) {
  } else {
    emlrtErrorWithMessageIdR2012b(&c_st, &e_emlrtRTEI, "MATLAB:dimagree", 0);
  }

  c_st.site = &o_emlrtRSI;
  if (1 > b->size[0]) {
    overflow = false;
  } else {
    overflow = (b->size[0] > 2147483646);
  }

  if (overflow) {
    d_st.site = &k_emlrtRSI;
    check_forloop_overflow_error(&d_st);
  }

  for (k = 0; k + 1 <= b->size[0]; k++) {
    y->data[k] = muDoubleScalarPower(a, b->data[k]);
  }
}

void d_power(const emlrtStack *sp, real_T a, const emxArray_real_T *b,
             emxArray_real_T *y)
{
  int32_T k;
  boolean_T overflow;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &l_emlrtRSI;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  b_st.site = &m_emlrtRSI;
  c_st.site = &n_emlrtRSI;
  k = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = b->size[1];
  emxEnsureCapacity(&c_st, (emxArray__common *)y, k, (int32_T)sizeof(real_T),
                    &b_emlrtRTEI);
  if (b_dimagree(y, b)) {
  } else {
    emlrtErrorWithMessageIdR2012b(&c_st, &e_emlrtRTEI, "MATLAB:dimagree", 0);
  }

  c_st.site = &o_emlrtRSI;
  if (1 > b->size[1]) {
    overflow = false;
  } else {
    overflow = (b->size[1] > 2147483646);
  }

  if (overflow) {
    d_st.site = &k_emlrtRSI;
    check_forloop_overflow_error(&d_st);
  }

  for (k = 0; k + 1 <= b->size[1]; k++) {
    y->data[k] = muDoubleScalarPower(a, b->data[k]);
  }
}

void e_power(const real_T a[96], real_T y[96])
{
  int32_T k;
  for (k = 0; k < 96; k++) {
    y[k] = muDoubleScalarPower(a[k], 2.0);
  }
}

void power(const real_T b[7], real_T y[7])
{
  int32_T k;
  for (k = 0; k < 7; k++) {
    y[k] = muDoubleScalarPower(10.0, b[k]);
  }
}

/* End of code generation (power.c) */
