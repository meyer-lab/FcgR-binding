/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorId_initialize.c
 *
 * Code generation for function 'NormalErrorId_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorId.h"
#include "NormalErrorId_initialize.h"
#include "_coder_NormalErrorId_mex.h"
#include "NormalErrorId_data.h"

/* Function Definitions */
void NormalErrorId_initialize(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtLicenseCheckR2012b(&st, "Statistics_Toolbox", 2);
  emlrtFirstTimeR2012b(emlrtRootTLSGlobal);
}

/* End of code generation (NormalErrorId_initialize.c) */
