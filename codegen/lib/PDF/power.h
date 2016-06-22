/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: power.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 22-Jun-2016 09:56:36
 */

#ifndef __POWER_H__
#define __POWER_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "PDF_types.h"

/* Function Declarations */
extern void b_power(const double b[24], double y[24]);
extern void c_power(double a, const emxArray_real_T *b, emxArray_real_T *y);
extern void d_power(double a, const emxArray_real_T *b, emxArray_real_T *y);
extern void power(const double b[7], double y[7]);

#endif

/*
 * File trailer for power.h
 *
 * [EOF]
 */
