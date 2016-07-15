/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalErrorId.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 15-Jul-2016 12:51:37
 */

#ifndef __NORMALERRORID_H__
#define __NORMALERRORID_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "NormalErrorId_types.h"

/* Function Declarations */
extern double NormalErrorId(const double Rtot[7], const double KdMat[60], const
  double mfiAdjMean[192], const double tnpbsa[2], const double meanPerCond[48],
  const double biCoefMat[900]);

#endif

/*
 * File trailer for NormalErrorId.h
 *
 * [EOF]
 */
