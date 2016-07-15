/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalError_initialize.c
 *
 * Code generation for function 'NormalError_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalError.h"
#include "NormalError_initialize.h"
#include "_coder_NormalError_mex.h"
#include "NormalError_data.h"

/* Function Definitions */
void NormalError_initialize(void)
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

/* End of code generation (NormalError_initialize.c) */
