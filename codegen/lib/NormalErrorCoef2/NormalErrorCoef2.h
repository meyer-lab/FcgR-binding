/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalErrorCoef2.h
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 15-Aug-2016 17:19:22
 */

#ifndef NORMALERRORCOEF2_H
#define NORMALERRORCOEF2_H

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "omp.h"
#include "NormalErrorCoef2_types.h"

/* Function Declarations */
extern double NormalErrorCoef2(const double Rtot[7], const double KdMat[60],
  const double mfiAdjMean[192], const double tnpbsa[2], const double
  meanPerCond[48], const double biCoefMat[900], double whichR);

#endif

/*
 * File trailer for NormalErrorCoef2.h
 *
 * [EOF]
 */
