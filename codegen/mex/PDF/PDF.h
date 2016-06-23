/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PDF.h
 *
 * Code generation for function 'PDF'
 *
 */

#ifndef __PDF_H__
#define __PDF_H__

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
extern real_T PDF(const emlrtStack *sp, const real_T x[7], const real_T kd[24],
                  const real_T mfiAdjMean[192], const real_T v[2], const real_T
                  biCoefMat[676], const real_T tnpbsa[2], const real_T
                  meanPerCond[48], const real_T stdPerCond[48]);

#ifdef __WATCOMC__

#pragma aux PDF value [8087];

#endif
#endif

/* End of code generation (PDF.h) */
