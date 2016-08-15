/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_NormalError_api.h
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 10-Aug-2016 17:24:40
 */

#ifndef _CODER_NORMALERROR_API_H
#define _CODER_NORMALERROR_API_H

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
extern real_T NormalError(real_T Rtot[12], real_T KdMat[60], real_T mfiAdjMean
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
