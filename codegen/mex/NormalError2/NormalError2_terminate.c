/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalError2_terminate.c
 *
 * Code generation for function 'NormalError2_terminate'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalError2.h"
#include "NormalError2_terminate.h"
#include "_coder_NormalError2_mex.h"
#include "NormalError2_data.h"

/* Function Definitions */
void NormalError2_atexit(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtEnterRtStackR2012b(&st);

  /* Free instance data */
  covrtFreeInstanceData(&emlrtCoverageInstance);

  /* Free instance data */
  covrtFreeInstanceData(&emlrtCoverageInstance);
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

void NormalError2_terminate(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/* End of code generation (NormalError2_terminate.c) */
