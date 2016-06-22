/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * power.h
 *
 * Code generation for function 'power'
 *
 */

#ifndef __POWER_H__
#define __POWER_H__

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
extern void b_power(const real_T b[24], real_T y[24]);
extern void c_power(const emlrtStack *sp, real_T a, const emxArray_real_T *b,
                    emxArray_real_T *y);
extern void d_power(const emlrtStack *sp, real_T a, const emxArray_real_T *b,
                    emxArray_real_T *y);
extern void e_power(const real_T a[96], real_T y[96]);
extern void power(const real_T b[7], real_T y[7]);

#endif

/* End of code generation (power.h) */
