/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef2_mexutil.h
 *
 * Code generation for function 'NormalErrorCoef2_mexutil'
 *
 */

#ifndef NORMALERRORCOEF2_MEXUTIL_H
#define NORMALERRORCOEF2_MEXUTIL_H

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
extern emlrtCTX emlrtGetRootTLSGlobal(void);
extern void emlrtLockerFunction(EmlrtLockeeFunction aLockee, const emlrtConstCTX
  aTLS, void *aData);

#endif

/* End of code generation (NormalErrorCoef2_mexutil.h) */
