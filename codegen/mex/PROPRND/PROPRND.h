/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PROPRND.h
 *
 * Code generation for function 'PROPRND'
 *
 */

#ifndef PROPRND_H
#define PROPRND_H

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
#include "PROPRND_types.h"

/* Function Declarations */
extern void PROPRND(const emlrtStack *sp, const real_T current[12], real_T lbR,
                    real_T ubR, real_T lbKx, real_T ubKx, real_T lbc, real_T ubc,
                    real_T lbv, real_T ubv, real_T lbsigma, real_T ubsigma,
                    real_T stdR, real_T stdKx, real_T stdc, real_T stdsigma,
                    real_T next[12]);

#endif

/* End of code generation (PROPRND.h) */
