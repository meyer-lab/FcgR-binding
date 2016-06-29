/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * randi.c
 *
 * Code generation for function 'randi'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "randi.h"
#include "pseudoAlgorithm_emxutil.h"

/* Variable Definitions */
static emlrtRSInfo k_emlrtRSI = { 60, "randi",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\randfun\\randi.m"
};

static emlrtRSInfo l_emlrtRSI = { 61, "randi",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\randfun\\randi.m"
};

static emlrtRTEInfo b_emlrtRTEI = { 1, 14, "randi",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\randfun\\randi.m"
};

static emlrtRTEInfo j_emlrtRTEI = { 53, 23, "assertValidSizeArg",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\assertValidSizeArg.m"
};

static emlrtRTEInfo k_emlrtRTEI = { 59, 15, "assertValidSizeArg",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\assertValidSizeArg.m"
};

/* Function Definitions */
void b_randi(const emlrtStack *sp, real_T varargin_1, emxArray_real_T *r)
{
  boolean_T p;
  real_T b_varargin_1;
  int32_T i3;
  int32_T k;
  emlrtStack st;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &k_emlrtRSI;
  if ((varargin_1 != varargin_1) || muDoubleScalarIsInf(varargin_1)) {
    p = false;
  } else {
    p = true;
  }

  if (p && (!(2.147483647E+9 < varargin_1))) {
    p = true;
  } else {
    p = false;
  }

  if (p) {
  } else {
    emlrtErrorWithMessageIdR2012b(&st, &j_emlrtRTEI,
      "Coder:MATLAB:NonIntegerInput", 4, 12, MIN_int32_T, 12, MAX_int32_T);
  }

  if (varargin_1 <= 0.0) {
    b_varargin_1 = 0.0;
  } else {
    b_varargin_1 = varargin_1;
  }

  if (2.147483647E+9 >= b_varargin_1) {
  } else {
    emlrtErrorWithMessageIdR2012b(&st, &k_emlrtRTEI, "Coder:MATLAB:pmaxsize", 0);
  }

  st.site = &l_emlrtRSI;
  i3 = r->size[0];
  r->size[0] = (int32_T)varargin_1;
  emxEnsureCapacity(&st, (emxArray__common *)r, i3, (int32_T)sizeof(real_T),
                    &b_emlrtRTEI);
  emlrtRandu(&r->data[0], r->size[0]);
  i3 = r->size[0];
  for (k = 0; k < i3; k++) {
    r->data[k] = 1.0 + muDoubleScalarFloor(r->data[k] * 26.0);
  }
}

void randi(const emlrtStack *sp, real_T varargin_1, emxArray_real_T *r)
{
  boolean_T p;
  real_T b_varargin_1;
  int32_T i2;
  int32_T k;
  emlrtStack st;
  st.prev = sp;
  st.tls = sp->tls;
  st.site = &k_emlrtRSI;
  if ((varargin_1 != varargin_1) || muDoubleScalarIsInf(varargin_1)) {
    p = false;
  } else {
    p = true;
  }

  if (p && (!(2.147483647E+9 < varargin_1))) {
    p = true;
  } else {
    p = false;
  }

  if (p) {
  } else {
    emlrtErrorWithMessageIdR2012b(&st, &j_emlrtRTEI,
      "Coder:MATLAB:NonIntegerInput", 4, 12, MIN_int32_T, 12, MAX_int32_T);
  }

  if (varargin_1 <= 0.0) {
    b_varargin_1 = 0.0;
  } else {
    b_varargin_1 = varargin_1;
  }

  if (2.147483647E+9 >= b_varargin_1) {
  } else {
    emlrtErrorWithMessageIdR2012b(&st, &k_emlrtRTEI, "Coder:MATLAB:pmaxsize", 0);
  }

  st.site = &l_emlrtRSI;
  i2 = r->size[0];
  r->size[0] = (int32_T)varargin_1;
  emxEnsureCapacity(&st, (emxArray__common *)r, i2, (int32_T)sizeof(real_T),
                    &b_emlrtRTEI);
  emlrtRandu(&r->data[0], r->size[0]);
  i2 = r->size[0];
  for (k = 0; k < i2; k++) {
    r->data[k] = 1.0 + muDoubleScalarFloor(r->data[k] * 4.0);
  }
}

/* End of code generation (randi.c) */
