/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * StoneMod.h
 *
 * Code generation for function 'StoneMod'
 *
 */

#ifndef STONEMOD_H
#define STONEMOD_H

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
#include "NormalError_types.h"

/* Function Declarations */
extern real_T StoneMod(const emlrtStack *sp, real_T logR, real_T Kd, real_T v,
  real_T logKx, real_T L0, const real_T biCoefMat[900]);

#ifdef __WATCOMC__

#pragma aux StoneMod value [8087];

#endif
#endif

/* End of code generation (StoneMod.h) */
