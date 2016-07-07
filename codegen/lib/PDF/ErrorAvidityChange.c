/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: ErrorAvidityChange.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 07-Jul-2016 12:53:52
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "ErrorAvidityChange.h"
#include "StoneSolver.h"
#include "PDF_rtwutil.h"

/* Function Definitions */

/*
 * Treats the last two elements of RtotTrue as the effective avidities of
 * TNP-4-BSA and TNP-26-BSA respectively (as of June 27, 2016, these are
 * elements 10 and 11). Runs Error.m inputting these two avidities as a
 * two-dimensional column vector which is passed into Error as the vector
 * v.
 * Arguments    : const double RtotTrue[11]
 *                const double Kd[60]
 *                const double mfiAdjMean[192]
 *                const double biCoefMat[676]
 *                double tnpbsa
 *                double *J
 *                double mfiExp_data[]
 *                int mfiExp_size[2]
 *                double mfiExpPre[48]
 * Return Type  : void
 */
void ErrorAvidityChange(const double RtotTrue[11], const double Kd[60], const
  double mfiAdjMean[192], const double biCoefMat[676], double tnpbsa, double *J,
  double mfiExp_data[], int mfiExp_size[2], double mfiExpPre[48])
{
  double x[2];
  int k;
  double Rtot[9];
  double Kx;
  double mfiExpPrePre[48];
  int j;
  int ixstart;
  int ix;
  boolean_T varargin_1[48];
  boolean_T maxval[8];
  int i;
  boolean_T mtmp;
  double y[192];
  double b_y[8];
  int iy;
  double s;

  /*  If error is called with Rtot being a single value, assume we want to */
  /*  have constant expression across all the receptors */
  for (k = 0; k < 2; k++) {
    x[k] = ceil(RtotTrue[k + 9]);
  }

  /* Convert from log scale */
  for (k = 0; k < 9; k++) {
    Rtot[k] = rt_powd_snf(10.0, RtotTrue[k]);
  }

  Kx = Rtot[6];

  /* Get expected value of MFIs (before conversion factors) from Equation 7 */
  /* from Stone */
  memset(&mfiExpPrePre[0], 0, 48U * sizeof(double));
  for (j = 0; j < 6; j++) {
    for (k = 0; k < 4; k++) {
      mfiExpPrePre[j + 6 * k] = StoneSolver(Rtot[j], Kx, x[0], Kd[j + 6 * k],
        tnpbsa, biCoefMat);
      mfiExpPrePre[j + 6 * (4 + k)] = StoneSolver(Rtot[j], Kx, x[1], Kd[j + 6 *
        k], tnpbsa, biCoefMat);
    }
  }

  /* Multiply by conversion factors */
  for (ixstart = 0; ixstart < 48; ixstart++) {
    mfiExpPre[ixstart] = Rtot[7] * mfiExpPrePre[ixstart];
  }

  for (ixstart = 0; ixstart < 4; ixstart++) {
    for (ix = 0; ix < 6; ix++) {
      mfiExpPre[ix + 6 * (4 + ixstart)] = Rtot[8] * mfiExpPrePre[ix + 6 * (4 +
        ixstart)];
    }
  }

  /* Check for undefined values (errors from ReqFuncSolver) */
  for (ixstart = 0; ixstart < 48; ixstart++) {
    varargin_1[ixstart] = (mfiExpPre[ixstart] == -1.0);
  }

  for (j = 0; j < 8; j++) {
    maxval[j] = varargin_1[6 * j];
    for (i = 0; i < 5; i++) {
      mtmp = maxval[j];
      if ((int)varargin_1[(i + 6 * j) + 1] > (int)maxval[j]) {
        mtmp = varargin_1[(i + 6 * j) + 1];
      }

      maxval[j] = mtmp;
    }
  }

  mtmp = maxval[0];
  for (ix = 0; ix < 7; ix++) {
    if ((int)maxval[ix + 1] > (int)mtmp) {
      mtmp = maxval[ix + 1];
    }
  }

  if (mtmp) {
    *J = 1.0E+8;
    mfiExp_size[0] = 6;
    mfiExp_size[1] = 8;
    for (ixstart = 0; ixstart < 48; ixstart++) {
      mfiExpPre[ixstart] = -1.0;
      mfiExp_data[ixstart] = -1.0;
    }
  } else {
    /* Create array of expected values to calculate residuals */
    mfiExp_size[0] = 24;
    mfiExp_size[1] = 8;
    for (j = 0; j < 6; j++) {
      for (k = 0; k < 4; k++) {
        ixstart = (j << 2) + k;
        for (ix = 0; ix < 4; ix++) {
          mfiExp_data[ixstart + 24 * ix] = mfiExpPre[j + 6 * k];
        }

        ixstart = (j << 2) + k;
        for (ix = 0; ix < 4; ix++) {
          mfiExp_data[ixstart + 24 * (4 + ix)] = mfiExpPre[j + 6 * (4 + k)];
        }
      }
    }

    /* Error */
    for (k = 0; k < 192; k++) {
      y[k] = rt_powd_snf(mfiExp_data[k] - mfiAdjMean[k], 2.0);
    }

    ix = -1;
    iy = -1;
    for (i = 0; i < 8; i++) {
      ixstart = ix + 1;
      ix++;
      if (!rtIsNaN(y[ixstart])) {
        s = y[ixstart];
      } else {
        s = 0.0;
      }

      for (k = 0; k < 23; k++) {
        ix++;
        if (!rtIsNaN(y[ix])) {
          s += y[ix];
        }
      }

      iy++;
      b_y[iy] = s;
    }

    *J = 0.0;
    for (k = 0; k < 8; k++) {
      if (!rtIsNaN(b_y[k])) {
        *J += b_y[k];
      }
    }
  }
}

/*
 * File trailer for ErrorAvidityChange.c
 *
 * [EOF]
 */
