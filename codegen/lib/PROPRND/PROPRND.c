/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PROPRND.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 27-Jul-2016 10:12:22
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "rand.h"

/* Function Definitions */

/*
 * Preset next below all minimum thresholds
 * Arguments    : const double current[12]
 *                double lbR
 *                double ubR
 *                double lbKx
 *                double ubKx
 *                double lbc
 *                double ubc
 *                double lbv
 *                double ubv
 *                double lbsigma
 *                double ubsigma
 *                double stdR
 *                double stdKx
 *                double stdc
 *                double stdsigma
 *                double next[12]
 * Return Type  : void
 */
void PROPRND(const double current[12], double lbR, double ubR, double lbKx,
             double ubKx, double lbc, double ubc, double lbv, double ubv, double
             lbsigma, double ubsigma, double stdR, double stdKx, double stdc,
             double stdsigma, double next[12])
{
  double b_lbR[12];
  int i0;
  int j;
  double NEXT;
  double x;
  double NEXT10;
  double NEXT11;
  double temp;
  for (i0 = 0; i0 < 6; i0++) {
    b_lbR[i0] = lbR;
  }

  b_lbR[6] = lbKx;
  for (i0 = 0; i0 < 2; i0++) {
    b_lbR[i0 + 7] = lbc;
  }

  b_lbR[9] = 1.0;
  b_lbR[10] = 1.0;
  b_lbR[11] = lbsigma;
  for (i0 = 0; i0 < 12; i0++) {
    next[i0] = b_lbR[i0] - 1.0;
  }

  /*  Generate new logR values */
  for (j = 0; j < 6; j++) {
    NEXT = next[j];
    while ((NEXT < lbR) || (ubR < NEXT)) {
      /*  inversestd represents the reciprocal of the standard deviation of the */
      /*  corresponding exponential distribution, which happens to be equal to */
      /*  the mean of the corresponding exponential distribution */
      /* -------------------------------------------------------------------------- */
      x = b_rand();
      x = log(x);
      x *= -stdR;
      if (stdR < 0.0) {
        x = rtNaN;
      }

      temp = c_rand();
      if (1.0 + floor(temp * 2.0) == 1.0) {
        x = -x;
      }

      NEXT = current[j] + x;
    }

    next[j] = NEXT;
  }

  /* Generate new logKx value */
  NEXT = next[6];
  while ((NEXT < lbKx) || (ubKx < NEXT)) {
    /*  inversestd represents the reciprocal of the standard deviation of the */
    /*  corresponding exponential distribution, which happens to be equal to */
    /*  the mean of the corresponding exponential distribution */
    /* -------------------------------------------------------------------------- */
    x = b_rand();
    x = log(x);
    x *= -stdKx;
    if (stdKx < 0.0) {
      x = rtNaN;
    }

    temp = c_rand();
    if (1.0 + floor(temp * 2.0) == 1.0) {
      x = -x;
    }

    NEXT = current[6] + x;
  }

  next[6] = NEXT;

  /* Generate new common logs of conversion coefficients */
  for (j = 0; j < 2; j++) {
    NEXT = next[j + 7];
    while ((NEXT < lbc) || (ubc < NEXT)) {
      /*  inversestd represents the reciprocal of the standard deviation of the */
      /*  corresponding exponential distribution, which happens to be equal to */
      /*  the mean of the corresponding exponential distribution */
      /* -------------------------------------------------------------------------- */
      x = b_rand();
      x = log(x);
      x *= -stdc;
      if (stdc < 0.0) {
        x = rtNaN;
      }

      temp = c_rand();
      if (1.0 + floor(temp * 2.0) == 1.0) {
        x = -x;
      }

      NEXT = current[j + 7] + x;
    }

    next[j + 7] = NEXT;
  }

  /* Generate new avidities     */
  NEXT10 = next[9];
  NEXT11 = next[10];
  while ((NEXT10 < lbv) || (ubv < NEXT10)) {
    x = c_rand();
    NEXT10 = (current[9] + (1.0 + floor(x * 3.0))) - 2.0;
  }

  next[9] = NEXT10;
  while ((NEXT11 < lbv) || (ubv < NEXT11)) {
    x = c_rand();
    NEXT11 = (current[10] + (1.0 + floor(x * 3.0))) - 2.0;
  }

  next[10] = NEXT11;

  /*  Generate next standard deviation coefficient */
  NEXT = next[11];
  while ((NEXT < lbsigma) || (ubsigma < NEXT)) {
    /*  inversestd represents the reciprocal of the standard deviation of the */
    /*  corresponding exponential distribution, which happens to be equal to */
    /*  the mean of the corresponding exponential distribution */
    /* -------------------------------------------------------------------------- */
    x = b_rand();
    x = log(x);
    x *= -stdsigma;
    if (stdsigma < 0.0) {
      x = rtNaN;
    }

    temp = c_rand();
    if (1.0 + floor(temp * 2.0) == 1.0) {
      x = -x;
    }

    NEXT = current[11] + x;
  }

  next[11] = NEXT;
}

/*
 * File trailer for PROPRND.c
 *
 * [EOF]
 */
