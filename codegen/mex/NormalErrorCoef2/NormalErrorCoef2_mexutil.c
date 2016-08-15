/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef2_mexutil.c
 *
 * Code generation for function 'NormalErrorCoef2_mexutil'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef2.h"
#include "NormalErrorCoef2_mexutil.h"
#include "NormalErrorCoef2_data.h"

/* Function Definitions */
emlrtCTX emlrtGetRootTLSGlobal(void)
{
  return emlrtRootTLSGlobal;
}

void emlrtLockerFunction(EmlrtLockeeFunction aLockee, const emlrtConstCTX aTLS,
  void *aData)
{
  omp_set_lock(&emlrtLockGlobal);
  emlrtCallLockeeFunction(aLockee, aTLS, aData);
  omp_unset_lock(&emlrtLockGlobal);
}

/* End of code generation (NormalErrorCoef2_mexutil.c) */
