/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: StoneSolver.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 23-Jun-2016 16:03:51
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "StoneSolver.h"
#include "power.h"
#include "PDF_rtwutil.h"

/* Function Definitions */

/*
 * Using the information given, finds the sum L presented in Equation 7
 * in Stone. In this context, all inputs save biCoefMat are scalars.
 * Arguments    : double Rtot
 *                double Kx
 *                double v
 *                double Kd
 *                double L0
 *                const double biCoefMat[676]
 * Return Type  : double
 */
double StoneSolver(double Rtot, double Kx, double v, double Kd, double L0, const
                   double biCoefMat[676])
{
  double L;
  double a;
  double b;
  double bVal;
  double cVal;
  double Req;
  int loop_ub;
  int ndbl;
  int apnd;
  int cdiff;
  double y_data[26];
  int k;
  double b_y_data[26];
  int y_size[2];
  int tmp_size[2];
  double tmp_data[26];
  double y;
  int b_y_size[2];

  /* Solve for Req, as described in Equation 2 in Stone */
  /* %%This function returns the point at which function fun equals zero */
  /* %%using the bisection algorithm. The closest a and b will converge to */
  /* %%in the algorithm is a distance 1e-12 apart. */
  /* -------------------------------------------------------------------------- */
  a = -20.0;
  b = log10(Rtot);

  /* -------------------------------------------------------------------------- */
  bVal = Rtot - rt_powd_snf(10.0, b) * (1.0 + v * L0 / Kd * rt_powd_snf(1.0 + Kx
    * rt_powd_snf(10.0, b), v - 1.0));

  /* -------------------------------------------------------------------------- */
  cVal = Rtot - 1.0000000000000001E-20 * (1.0 + v * L0 / Kd * rt_powd_snf(1.0 +
    Kx * 1.0000000000000001E-20, v - 1.0));

  /*  Is there no root within the interval? */
  if (bVal * cVal > 0.0) {
    Req = 1000.0;
  } else {
    /* In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin */
    /* with; only implemented for MATLAB Coder */
    Req = 1000.0;

    /* Commence algorithm */
    while ((b - a > 0.0001) || (fabs(cVal) > 0.0001)) {
      Req = (a + b) / 2.0;

      /* -------------------------------------------------------------------------- */
      cVal = Rtot - rt_powd_snf(10.0, Req) * (1.0 + v * L0 / Kd * rt_powd_snf
        (1.0 + Kx * rt_powd_snf(10.0, Req), v - 1.0));
      if (cVal * bVal >= 0.0) {
        b = Req;
        bVal = cVal;
      } else {
        a = Req;
      }
    }
  }

  /* Check for error output from ReqFuncSolver */
  if (Req == 1000.0) {
    L = -1.0;
  } else {
    /* Convert from logarithmic scale */
    Req = rt_powd_snf(10.0, Req);
    if (1.0 > v) {
      loop_ub = 0;
    } else {
      loop_ub = (int)v;
    }

    ndbl = (int)floor((v - 1.0) + 0.5);
    apnd = ndbl + 1;
    cdiff = (ndbl - (int)v) + 1;
    if (fabs(cdiff) < 4.4408920985006262E-16 * (double)(int)v) {
      ndbl++;
      apnd = (int)v;
    } else if (cdiff > 0) {
      apnd = ndbl;
    } else {
      ndbl++;
    }

    if (ndbl > 0) {
      y_data[0] = 1.0;
      if (ndbl > 1) {
        y_data[ndbl - 1] = apnd;
        cdiff = ndbl - 1;
        cdiff /= 2;
        for (k = 1; k < cdiff; k++) {
          y_data[k] = 1.0 + (double)k;
          y_data[(ndbl - k) - 1] = apnd - k;
        }

        if (cdiff << 1 == ndbl - 1) {
          y_data[cdiff] = (1.0 + (double)apnd) / 2.0;
        } else {
          y_data[cdiff] = 1.0 + (double)cdiff;
          y_data[cdiff + 1] = apnd - cdiff;
        }
      }
    }

    y_size[0] = 1;
    y_size[1] = ndbl;
    for (cdiff = 0; cdiff < ndbl; cdiff++) {
      b_y_data[cdiff] = y_data[cdiff] - 1.0;
    }

    power(Kx, b_y_data, y_size, tmp_data, tmp_size);
    y = L0 / Kd;
    ndbl = (int)floor((v - 1.0) + 0.5);
    apnd = ndbl + 1;
    cdiff = (ndbl - (int)v) + 1;
    if (fabs(cdiff) < 4.4408920985006262E-16 * (double)(int)v) {
      ndbl++;
      apnd = (int)v;
    } else if (cdiff > 0) {
      apnd = ndbl;
    } else {
      ndbl++;
    }

    b_y_size[0] = 1;
    b_y_size[1] = ndbl;
    if (ndbl > 0) {
      y_data[0] = 1.0;
      if (ndbl > 1) {
        y_data[ndbl - 1] = apnd;
        cdiff = ndbl - 1;
        cdiff /= 2;
        for (k = 1; k < cdiff; k++) {
          y_data[k] = 1.0 + (double)k;
          y_data[(ndbl - k) - 1] = apnd - k;
        }

        if (cdiff << 1 == ndbl - 1) {
          y_data[cdiff] = (1.0 + (double)apnd) / 2.0;
        } else {
          y_data[cdiff] = 1.0 + (double)cdiff;
          y_data[cdiff + 1] = apnd - cdiff;
        }
      }
    }

    power(Req, y_data, b_y_size, b_y_data, y_size);
    for (cdiff = 0; cdiff < loop_ub; cdiff++) {
      y_data[cdiff] = y * (biCoefMat[cdiff + 26 * ((int)v - 1)] *
                           tmp_data[tmp_size[0] * cdiff]) * b_y_data[y_size[0] *
        cdiff];
    }

    if (loop_ub == 0) {
      L = 0.0;
    } else {
      L = y_data[0];
      for (k = 2; k <= loop_ub; k++) {
        L += y_data[k - 1];
      }
    }
  }

  return L;
}

/*
 * File trailer for StoneSolver.c
 *
 * [EOF]
 */
