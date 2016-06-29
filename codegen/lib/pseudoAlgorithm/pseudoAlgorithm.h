/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: pseudoAlgorithm.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

#ifndef __PSEUDOALGORITHM_H__
#define __PSEUDOALGORITHM_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "pseudoAlgorithm_types.h"

/* Function Declarations */
extern void pseudoAlgorithm(double nsamples, double goodsize, double mehsize,
  const double kdBruhns[24], const double tnpbsa[2], const double mfiAdjMean[192],
  const double best[7], const double meanPerCond[48], const double stdPerCond[48],
  const double biCoefMat[676], emxArray_real_T *good, emxArray_real_T *goodfit,
  emxArray_real_T *meh);

#endif

/*
 * File trailer for pseudoAlgorithm.h
 *
 * [EOF]
 */
