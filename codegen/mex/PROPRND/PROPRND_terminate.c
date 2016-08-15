/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PROPRND_terminate.c
 *
 * Code generation for function 'PROPRND_terminate'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "PROPRND_terminate.h"
#include "_coder_PROPRND_mex.h"
#include "PROPRND_data.h"

/* Function Definitions */
void PROPRND_atexit(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtEnterRtStackR2012b(&st);

  /* Free instance data */
  covrtFreeInstanceData(&emlrtCoverageInstance);
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

void PROPRND_terminate(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/* End of code generation (PROPRND_terminate.c) */
