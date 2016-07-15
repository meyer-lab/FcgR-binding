/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalError.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 15-Jul-2016 09:48:12
 */

#ifndef __NORMALERROR_H__
#define __NORMALERROR_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "NormalError_types.h"

/* Function Declarations */
extern double NormalError(const double Rtot[13], const double KdMat[60], const
  double mfiAdjMean[192], const double tnpbsa[2], const double meanPerCond[48],
  const double biCoefMat[900]);

#endif

/*
 * File trailer for NormalError.h
 *
 * [EOF]
 */
