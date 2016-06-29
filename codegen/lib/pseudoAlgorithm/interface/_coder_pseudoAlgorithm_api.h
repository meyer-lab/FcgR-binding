/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: _coder_pseudoAlgorithm_api.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

#ifndef ___CODER_PSEUDOALGORITHM_API_H__
#define ___CODER_PSEUDOALGORITHM_API_H__

/* Include Files */
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include <stddef.h>
#include <stdlib.h>
#include "_coder_pseudoAlgorithm_api.h"

/* Type Definitions */
#ifndef struct_emxArray_real_T
#define struct_emxArray_real_T

struct emxArray_real_T
{
  real_T *data;
  int32_T *size;
  int32_T allocatedSize;
  int32_T numDimensions;
  boolean_T canFreeData;
};

#endif                                 /*struct_emxArray_real_T*/

#ifndef typedef_emxArray_real_T
#define typedef_emxArray_real_T

typedef struct emxArray_real_T emxArray_real_T;

#endif                                 /*typedef_emxArray_real_T*/

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

/* Function Declarations */
extern void pseudoAlgorithm(real_T nsamples, real_T goodsize, real_T mehsize,
  real_T kdBruhns[24], real_T tnpbsa[2], real_T mfiAdjMean[192], real_T best[7],
  real_T meanPerCond[48], real_T stdPerCond[48], real_T biCoefMat[676],
  emxArray_real_T *good, emxArray_real_T *goodfit, emxArray_real_T *meh);
extern void pseudoAlgorithm_api(const mxArray *prhs[10], const mxArray *plhs[3]);
extern void pseudoAlgorithm_atexit(void);
extern void pseudoAlgorithm_initialize(void);
extern void pseudoAlgorithm_terminate(void);
extern void pseudoAlgorithm_xil_terminate(void);

#endif

/*
 * File trailer for _coder_pseudoAlgorithm_api.h
 *
 * [EOF]
 */
