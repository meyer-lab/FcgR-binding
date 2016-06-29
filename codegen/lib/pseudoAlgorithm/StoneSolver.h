/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: StoneSolver.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

#ifndef __STONESOLVER_H__
#define __STONESOLVER_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "pseudoAlgorithm_types.h"

/* Function Declarations */
extern double StoneSolver(double Rtot, double Kx, double v, double Kd, double L0,
  const double biCoefMat[676]);

#endif

/*
 * File trailer for StoneSolver.h
 *
 * [EOF]
 */
