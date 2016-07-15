/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_NormalError_api.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 15-Jul-2016 09:48:12
 */

#ifndef ___CODER_NORMALERROR_API_H__
#define ___CODER_NORMALERROR_API_H__

/* Include Files */
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include <stddef.h>
#include <stdlib.h>
#include "_coder_NormalError_api.h"

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

/* Function Declarations */
extern real_T NormalError(real_T Rtot[13], real_T KdMat[60], real_T mfiAdjMean
  [192], real_T tnpbsa[2], real_T meanPerCond[48], real_T biCoefMat[900]);
extern void NormalError_api(const mxArray *prhs[6], const mxArray *plhs[1]);
extern void NormalError_atexit(void);
extern void NormalError_initialize(void);
extern void NormalError_terminate(void);
extern void NormalError_xil_terminate(void);

#endif

/*
 * File trailer for _coder_NormalError_api.h
 *
 * [EOF]
 */
