/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: Error.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 22-Jun-2016 09:56:36
 */

#ifndef __ERROR_H__
#define __ERROR_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "PDF_types.h"

/* Function Declarations */
extern void Error(double Rtot[7], const double kd[24], const double mfiAdjMean4
                  [96], const double mfiAdjMean26[96], const double v[2], const
                  double biCoefMat[676], const double tnpbsa[2], double *J,
                  double mfiExp_data[], int mfiExp_size[2], double
                  mfiExpPre_data[], int mfiExpPre_size[2]);

#endif

/*
 * File trailer for Error.h
 *
 * [EOF]
 */
