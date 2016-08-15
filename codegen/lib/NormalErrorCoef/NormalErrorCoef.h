/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalErrorCoef.h
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 15-Aug-2016 16:41:41
 */

#ifndef NORMALERRORCOEF_H
#define NORMALERRORCOEF_H

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "NormalErrorCoef_types.h"

/* Function Declarations */
extern double NormalErrorCoef(const double Rtot[12], const double KdMat[60],
  const double mfiAdjMean[192], const double tnpbsa[2], const double
  meanPerCond[48], const double biCoefMat[900]);

#endif

/*
 * File trailer for NormalErrorCoef.h
 *
 * [EOF]
 */
