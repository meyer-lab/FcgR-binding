/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef.h
 *
 * Code generation for function 'NormalErrorCoef'
 *
 */

#ifndef NORMALERRORCOEF_H
#define NORMALERRORCOEF_H

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
#include "NormalErrorCoef_types.h"

/* Function Declarations */
extern real_T NormalErrorCoef(const emlrtStack *sp, const real_T Rtot[12], const
  real_T KdMat[60], const real_T mfiAdjMean[192], const real_T tnpbsa[2], const
  real_T meanPerCond[48], const real_T biCoefMat[900]);

#ifdef __WATCOMC__

#pragma aux NormalErrorCoef value [8087];

#endif
#endif

/* End of code generation (NormalErrorCoef.h) */
