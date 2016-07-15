/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalError.h
 *
 * Code generation for function 'NormalError'
 *
 */

#ifndef __NORMALERROR_H__
#define __NORMALERROR_H__

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
#include "NormalError_types.h"

/* Function Declarations */
extern real_T NormalError(const emlrtStack *sp, const real_T Rtot[13], const
  real_T KdMat[60], const real_T mfiAdjMean[192], const real_T tnpbsa[2], const
  real_T meanPerCond[48], const real_T biCoefMat[900]);

#ifdef __WATCOMC__

#pragma aux NormalError value [8087];

#endif
#endif

/* End of code generation (NormalError.h) */
