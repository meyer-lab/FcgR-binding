/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef_terminate.c
 *
 * Code generation for function 'NormalErrorCoef_terminate'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef.h"
#include "NormalErrorCoef_terminate.h"
#include "_coder_NormalErrorCoef_mex.h"
#include "NormalErrorCoef_data.h"

/* Function Definitions */
void NormalErrorCoef_atexit(void)
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

void NormalErrorCoef_terminate(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/* End of code generation (NormalErrorCoef_terminate.c) */
