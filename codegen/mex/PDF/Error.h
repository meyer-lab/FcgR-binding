/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Error.h
 *
 * Code generation for function 'Error'
 *
 */

#ifndef __ERROR_H__
#define __ERROR_H__

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
extern void Error(const emlrtStack *sp, real_T Rtot[9], const real_T Kd[60],
                  const real_T mfiAdjMean[192], const real_T v[2], const real_T
                  biCoefMat[676], real_T tnpbsa, real_T *J, real_T mfiExp_data[],
                  int32_T mfiExp_size[2], real_T mfiExpPre[48]);

#endif

/* End of code generation (Error.h) */
