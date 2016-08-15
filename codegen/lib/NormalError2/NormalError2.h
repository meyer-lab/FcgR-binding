/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalError2.h
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 10-Aug-2016 17:28:35
 */

#ifndef NORMALERROR2_H
#define NORMALERROR2_H

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "NormalError2_types.h"

/* Function Declarations */
extern double NormalError2(const double Rtot[7], const double KdMat[60], const
  double mfiAdjMean[192], const double tnpbsa[2], const double meanPerCond[48],
  const double biCoefMat[900], double whichR);

#endif

/*
 * File trailer for NormalError2.h
 *
 * [EOF]
 */
