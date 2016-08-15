/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef2.h
 *
 * Code generation for function 'NormalErrorCoef2'
 *
 */

#ifndef NORMALERRORCOEF2_H
#define NORMALERRORCOEF2_H

/* Include files */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mwmathutil.h"
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include "covrt.h"
#include "rtwtypes.h"
#include "omp.h"
#include "NormalErrorCoef2_types.h"

/* Function Declarations */
extern real_T NormalErrorCoef2(const emlrtStack *sp, const real_T Rtot[7], const
  real_T KdMat[60], const real_T mfiAdjMean[192], const real_T tnpbsa[2], const
  real_T meanPerCond[48], const real_T biCoefMat[900], real_T whichR);

#ifdef __WATCOMC__

#pragma aux NormalErrorCoef2 value [8087];

#endif
#endif

/* End of code generation (NormalErrorCoef2.h) */
