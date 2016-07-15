/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_NormalErrorId_api.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 15-Jul-2016 12:51:37
 */

#ifndef ___CODER_NORMALERRORID_API_H__
#define ___CODER_NORMALERRORID_API_H__

/* Include Files */
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include <stddef.h>
#include <stdlib.h>
#include "_coder_NormalErrorId_api.h"

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

/* Function Declarations */
extern real_T NormalErrorId(real_T Rtot[7], real_T KdMat[60], real_T mfiAdjMean
  [192], real_T tnpbsa[2], real_T meanPerCond[48], real_T biCoefMat[900]);
extern void NormalErrorId_api(const mxArray *prhs[6], const mxArray *plhs[1]);
extern void NormalErrorId_atexit(void);
extern void NormalErrorId_initialize(void);
extern void NormalErrorId_terminate(void);
extern void NormalErrorId_xil_terminate(void);

#endif

/*
 * File trailer for _coder_NormalErrorId_api.h
 *
 * [EOF]
 */
