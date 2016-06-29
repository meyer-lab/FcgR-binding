/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: ErrorAvidityChange.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

#ifndef __ERRORAVIDITYCHANGE_H__
#define __ERRORAVIDITYCHANGE_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "pseudoAlgorithm_types.h"

/* Function Declarations */
extern void ErrorAvidityChange(const double RtotTrue[11], const double Kd[24],
  const double mfiAdjMean[192], const double biCoefMat[676], const double
  tnpbsa[2], double *J, double mfiExp_data[], int mfiExp_size[2], double
  mfiExpPre[48]);

#endif

/*
 * File trailer for ErrorAvidityChange.h
 *
 * [EOF]
 */
