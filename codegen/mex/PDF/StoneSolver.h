/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * StoneSolver.h
 *
 * Code generation for function 'StoneSolver'
 *
 */

#ifndef __STONESOLVER_H__
#define __STONESOLVER_H__

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
#include "PDF_types.h"

/* Function Declarations */
extern real_T StoneSolver(const emlrtStack *sp, real_T Rtot, real_T Kx, real_T v,
  real_T Kd, real_T L0, const real_T biCoefMat[676]);

#ifdef __WATCOMC__

#pragma aux StoneSolver value [8087];

#endif
#endif

/* End of code generation (StoneSolver.h) */
