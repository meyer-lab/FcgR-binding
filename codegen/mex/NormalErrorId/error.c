/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * error.c
 *
 * Code generation for function 'error'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorId.h"
#include "error.h"

/* Variable Definitions */
static emlrtRTEInfo emlrtRTEI = { 17, 9, "error",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\eml\\+coder\\+internal\\error.m"
};

/* Function Definitions */
void error(const emlrtStack *sp)
{
  static const char_T varargin_1[3] = { 'l', 'o', 'g' };

  emlrtErrorWithMessageIdR2012b(sp, &emlrtRTEI, "Coder:toolbox:ElFunDomainError",
    3, 4, 3, varargin_1);
}

/* End of code generation (error.c) */
