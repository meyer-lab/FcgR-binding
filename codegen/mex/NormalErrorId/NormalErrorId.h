/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorId.h
 *
 * Code generation for function 'NormalErrorId'
 *
 */

#ifndef __NORMALERRORID_H__
#define __NORMALERRORID_H__

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
#include "NormalErrorId_types.h"

/* Function Declarations */
extern real_T NormalErrorId(const emlrtStack *sp, const real_T Rtot[7], const
  real_T KdMat[60], const real_T mfiAdjMean[192], const real_T tnpbsa[2], const
  real_T meanPerCond[48], const real_T biCoefMat[900]);

#ifdef __WATCOMC__

#pragma aux NormalErrorId value [8087];

#endif
#endif

/* End of code generation (NormalErrorId.h) */
