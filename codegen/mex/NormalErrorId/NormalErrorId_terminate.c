/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorId_terminate.c
 *
 * Code generation for function 'NormalErrorId_terminate'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorId.h"
#include "NormalErrorId_terminate.h"
#include "_coder_NormalErrorId_mex.h"
#include "NormalErrorId_data.h"

/* Function Definitions */
void NormalErrorId_atexit(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtEnterRtStackR2012b(&st);
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

void NormalErrorId_terminate(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/* End of code generation (NormalErrorId_terminate.c) */
