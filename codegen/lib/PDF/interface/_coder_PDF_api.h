/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_PDF_api.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 27-Jun-2016 22:01:50
 */

#ifndef ___CODER_PDF_API_H__
#define ___CODER_PDF_API_H__

/* Include Files */
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include <stddef.h>
#include <stdlib.h>
#include "_coder_PDF_api.h"

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

/* Function Declarations */
extern real_T PDF(real_T x[11], real_T kd[24], real_T mfiAdjMean[192], real_T
                  biCoefMat[676], real_T tnpbsa[2], real_T meanPerCond[48],
                  real_T stdPerCond[48]);
extern void PDF_api(const mxArray *prhs[7], const mxArray *plhs[1]);
extern void PDF_atexit(void);
extern void PDF_initialize(void);
extern void PDF_terminate(void);
extern void PDF_xil_terminate(void);

#endif

/*
 * File trailer for _coder_PDF_api.h
 *
 * [EOF]
 */
