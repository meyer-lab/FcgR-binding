/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_NormalErrorCoef2_api.h
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 15-Aug-2016 16:47:28
 */

#ifndef _CODER_NORMALERRORCOEF2_API_H
#define _CODER_NORMALERRORCOEF2_API_H

/* Include Files */
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include <stddef.h>
#include <stdlib.h>
#include "_coder_NormalErrorCoef2_api.h"

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

/* Function Declarations */
extern real_T NormalErrorCoef2(real_T Rtot[12], real_T KdMat[60], real_T
  mfiAdjMean[192], real_T tnpbsa[2], real_T meanPerCond[48], real_T biCoefMat
  [900], real_T whichR);
extern void NormalErrorCoef2_api(const mxArray *prhs[7], const mxArray *plhs[1]);
extern void NormalErrorCoef2_atexit(void);
extern void NormalErrorCoef2_initialize(void);
extern void NormalErrorCoef2_terminate(void);
extern void NormalErrorCoef2_xil_terminate(void);

#endif

/*
 * File trailer for _coder_NormalErrorCoef2_api.h
 *
 * [EOF]
 */
