/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PROPRND.h
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 27-Jul-2016 10:12:22
 */

#ifndef PROPRND_H
#define PROPRND_H

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "PROPRND_types.h"

/* Function Declarations */
extern void PROPRND(const double current[12], double lbR, double ubR, double
                    lbKx, double ubKx, double lbc, double ubc, double lbv,
                    double ubv, double lbsigma, double ubsigma, double stdR,
                    double stdKx, double stdc, double stdsigma, double next[12]);

#endif

/*
 * File trailer for PROPRND.h
 *
 * [EOF]
 */
