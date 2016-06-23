/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PDF.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 23-Jun-2016 16:03:51
 */

#ifndef __PDF_H__
#define __PDF_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "PDF_types.h"

/* Function Declarations */
extern double PDF(const double x[7], const double kd[24], const double
                  mfiAdjMean[192], const double v[2], const double biCoefMat[676],
                  const double tnpbsa[2], const double meanPerCond[48], const
                  double stdPerCond[48]);

#endif

/*
 * File trailer for PDF.h
 *
 * [EOF]
 */
