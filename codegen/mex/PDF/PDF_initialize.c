/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PDF_initialize.c
 *
 * Code generation for function 'PDF_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "PDF_initialize.h"
#include "_coder_PDF_mex.h"
#include "PDF_data.h"

/* Function Definitions */
void PDF_initialize(void)
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

/* End of code generation (PDF_initialize.c) */
