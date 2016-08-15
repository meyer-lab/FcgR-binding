/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: StoneMod.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 15-Aug-2016 16:47:28
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef2.h"
#include "StoneMod.h"
#include "power.h"
#include "NormalErrorCoef2_rtwutil.h"

/* Function Definitions */

/*
 * Returns the number of mutlivalent ligand bound to a cell with 10^logR
 * receptors, granted each epitope of the ligand binds to the receptor
 * kind in question with dissociation constant Kd and cross-links with
 * other receptors with crosslinking constant Kx = 10^logKx. All
 * equations derived from Stone et al. (2001). Assumed that ligand is at
 * saturating concentration L0 = 7e-8 M, which is as it is (approximately)
 * for TNP-4-BSA in Lux et al. (2013).
 * Arguments    : double logR
 *                double Kd
 *                double v
 *                double logKx
 *                double L0
 *                const double biCoefMat[900]
 * Return Type  : double
 */
double StoneMod(double logR, double Kd, double v, double logKx, double L0, const
                double biCoefMat[900])
{
  double L;
  double Kx;
  double R;
  int loop_ub;
  double viLikdi;
  double a;
  double b;
  double x;
  double bVal;
  double cVal;
  double c;
  int ndbl;
  int apnd;
  int cdiff;
  double y_data[30];
  double b_y_data[30];
  int y_size[2];
  int k;
  double tmp_data[30];
  int tmp_size[2];
  int b_y_size[2];
  Kx = rt_powd_snf(10.0, logKx);
  R = rt_powd_snf(10.0, logR);

  /* Vector of binomial coefficients */
  if (1.0 > v) {
    loop_ub = 0;
  } else {
    loop_ub = (int)v;
  }

  /* %%This function returns the point at which function fun equals zero */
  /* %%using the bisection algorithm. The closest a and b will converge to */
  /* %%in the algorithm is a distance 1e-12 apart. */
  /* -------------------------------------------------------------------------- */
  viLikdi = v * L0 / Kd;
  a = -20.0;
  b = log10(R);

  /* -------------------------------------------------------------------------- */
  x = rt_powd_snf(10.0, b);
  bVal = R - x * (1.0 + viLikdi * rt_powd_snf(1.0 + Kx * x, v - 1.0));

  /* -------------------------------------------------------------------------- */
  cVal = R - 1.0000000000000001E-20 * (1.0 + viLikdi * rt_powd_snf(1.0 + Kx *
    1.0000000000000001E-20, v - 1.0));

  /*  Is there no root within the interval? */
  if (bVal * cVal > 0.0) {
    c = 1000.0;
  } else {
    /* In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin */
    /* with; only implemented for MATLAB Coder */
    c = 1000.0;

    /* Commence algorithm */
    while ((b - a > 0.0001) && (fabs(cVal) > 0.0001)) {
      c = (a + b) / 2.0;

      /* -------------------------------------------------------------------------- */
      x = rt_powd_snf(10.0, c);
      cVal = R - x * (1.0 + viLikdi * rt_powd_snf(1.0 + Kx * x, v - 1.0));
      if (cVal * bVal >= 0.0) {
        b = c;
        bVal = cVal;
      } else {
        a = c;
      }
    }
  }

  /* Calculate L, according to equations 1 and 7 */
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
      cdiff = (ndbl - 1) / 2;
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
  x = L0 / Kd;
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
      cdiff = (ndbl - 1) / 2;
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

  power(rt_powd_snf(10.0, c), y_data, b_y_size, b_y_data, y_size);
  for (cdiff = 0; cdiff < loop_ub; cdiff++) {
    y_data[cdiff] = biCoefMat[cdiff + 30 * ((int)v - 1)] * tmp_data[tmp_size[0] *
      cdiff] * (x * b_y_data[y_size[0] * cdiff]);
  }

  if (loop_ub == 0) {
    L = 0.0;
  } else {
    L = y_data[0];
    for (k = 2; k <= loop_ub; k++) {
      L += y_data[k - 1];
    }
  }

  return L;
}

/*
 * File trailer for StoneMod.c
 *
 * [EOF]
 */
