/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_pseudoAlgorithm_mex.c
 *
 * Code generation for function '_coder_pseudoAlgorithm_mex'
 *
 */

/* Include files */
#include "pseudoAlgorithm.h"
#include "_coder_pseudoAlgorithm_mex.h"
#include "pseudoAlgorithm_terminate.h"
#include "_coder_pseudoAlgorithm_api.h"
#include "pseudoAlgorithm_initialize.h"
#include "pseudoAlgorithm_data.h"

/* Function Declarations */
static void pseudoAlgorithm_mexFunction(int32_T nlhs, mxArray *plhs[3], int32_T
  nrhs, const mxArray *prhs[10]);

/* Function Definitions */
static void pseudoAlgorithm_mexFunction(int32_T nlhs, mxArray *plhs[3], int32_T
  nrhs, const mxArray *prhs[10])
{
  int32_T n;
  const mxArray *inputs[10];
  const mxArray *outputs[3];
  int32_T b_nlhs;
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;

  /* Check for proper number of arguments. */
  if (nrhs != 10) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:WrongNumberOfInputs", 5, 12, 10, 4,
                        15, "pseudoAlgorithm");
  }

  if (nlhs > 3) {
    emlrtErrMsgIdAndTxt(&st, "EMLRT:runTime:TooManyOutputArguments", 3, 4, 15,
                        "pseudoAlgorithm");
  }

  /* Temporary copy for mex inputs. */
  for (n = 0; n < nrhs; n++) {
    inputs[n] = prhs[n];
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(&st);
    }
  }

  /* Call the function. */
  pseudoAlgorithm_api(inputs, outputs);

  /* Copy over outputs to the caller. */
  if (nlhs < 1) {
    b_nlhs = 1;
  } else {
    b_nlhs = nlhs;
  }

  emlrtReturnArrays(b_nlhs, plhs, outputs);

  /* Module termination. */
  pseudoAlgorithm_terminate();
}

void mexFunction(int32_T nlhs, mxArray *plhs[], int32_T nrhs, const mxArray
                 *prhs[])
{
  mexAtExit(pseudoAlgorithm_atexit);

  /* Initialize the memory manager. */
  /* Module initialization. */
  pseudoAlgorithm_initialize();

  /* Dispatch the entry-point. */
  pseudoAlgorithm_mexFunction(nlhs, plhs, nrhs, prhs);
}

emlrtCTX mexFunctionCreateRootTLS(void)
{
  emlrtCreateRootTLS(&emlrtRootTLSGlobal, &emlrtContextGlobal, NULL, 1);
  return emlrtRootTLSGlobal;
}

/* End of code generation (_coder_pseudoAlgorithm_mex.c) */
