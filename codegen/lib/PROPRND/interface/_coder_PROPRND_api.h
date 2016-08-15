/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_PROPRND_api.h
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 27-Jul-2016 10:12:22
 */

#ifndef _CODER_PROPRND_API_H
#define _CODER_PROPRND_API_H

/* Include Files */
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include <stddef.h>
#include <stdlib.h>
#include "_coder_PROPRND_api.h"

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

/* Function Declarations */
extern void PROPRND(real_T current[12], real_T lbR, real_T ubR, real_T lbKx,
                    real_T ubKx, real_T lbc, real_T ubc, real_T lbv, real_T ubv,
                    real_T lbsigma, real_T ubsigma, real_T stdR, real_T stdKx,
                    real_T stdc, real_T stdsigma, real_T next[12]);
extern void PROPRND_api(const mxArray *prhs[15], const mxArray *plhs[1]);
extern void PROPRND_atexit(void);
extern void PROPRND_initialize(void);
extern void PROPRND_terminate(void);
extern void PROPRND_xil_terminate(void);

#endif

/*
 * File trailer for _coder_PROPRND_api.h
 *
 * [EOF]
 */
