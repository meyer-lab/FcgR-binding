/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * pseudoAlgorithm.h
 *
 * Code generation for function 'pseudoAlgorithm'
 *
 */

#ifndef __PSEUDOALGORITHM_H__
#define __PSEUDOALGORITHM_H__

/* Include files */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mwmathutil.h"
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include "blas.h"
#include "rtwtypes.h"
#include "pseudoAlgorithm_types.h"

/* Function Declarations */
extern void pseudoAlgorithm(const emlrtStack *sp, real_T nsamples, real_T
  goodsize, real_T mehsize, const real_T kdBruhns[24], const real_T tnpbsa[2],
  const real_T mfiAdjMean[192], const real_T best[7], const real_T meanPerCond
  [48], const real_T stdPerCond[48], const real_T biCoefMat[676],
  emxArray_real_T *good, emxArray_real_T *goodfit, emxArray_real_T *meh);

#endif

/* End of code generation (pseudoAlgorithm.h) */
