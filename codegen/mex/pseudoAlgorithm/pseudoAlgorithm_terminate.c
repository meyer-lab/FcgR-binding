/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * pseudoAlgorithm_terminate.c
 *
 * Code generation for function 'pseudoAlgorithm_terminate'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "pseudoAlgorithm_terminate.h"
#include "_coder_pseudoAlgorithm_mex.h"
#include "pseudoAlgorithm_data.h"

/* Function Definitions */
void pseudoAlgorithm_atexit(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtEnterRtStackR2012b(&st);
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

void pseudoAlgorithm_terminate(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/* End of code generation (pseudoAlgorithm_terminate.c) */
