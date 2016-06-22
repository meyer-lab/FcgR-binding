/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * nansum.h
 *
 * Code generation for function 'nansum'
 *
 */

#ifndef __NANSUM_H__
#define __NANSUM_H__

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
extern real_T b_nansum(const real_T varargin_1[8]);

#ifdef __WATCOMC__

#pragma aux b_nansum value [8087];

#endif

extern real_T nansum(const emlrtStack *sp, const real_T varargin_1_data[], const
                     int32_T varargin_1_size[1]);

#ifdef __WATCOMC__

#pragma aux nansum value [8087];

#endif
#endif

/* End of code generation (nansum.h) */
