/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalError.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 10-Aug-2016 17:24:40
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalError.h"
#include "StoneMod.h"
#include "power.h"
#include "NormalError_rtwutil.h"

/* Function Definitions */

/*
 * Arguments    : const double Rtot[12]
 *                const double KdMat[60]
 *                const double mfiAdjMean[192]
 *                const double tnpbsa[2]
 *                const double meanPerCond[48]
 *                const double biCoefMat[900]
 * Return Type  : double
 */
double NormalError(const double Rtot[12], const double KdMat[60], const double
                   mfiAdjMean[192], const double tnpbsa[2], const double
                   meanPerCond[48], const double biCoefMat[900])
{
  double logSqrErr;
  double sigCoef;
  double logSqrErrMat[192];
  int j;
  double y[8];
  double c;
  int ix;
  int ixstart;
  int iy;
  int i;
  int l;
  double MFI;
  int m;
  double s;
  double z;
  sigCoef = rt_powd_snf(10.0, Rtot[11]);
  for (j = 0; j < 2; j++) {
    c = rt_powd_snf(10.0, Rtot[7 + j]);
    for (ixstart = 0; ixstart < 6; ixstart++) {
      for (l = 0; l < 4; l++) {
        MFI = c * StoneMod(Rtot[ixstart], KdMat[ixstart + 6 * l], Rtot[9 + j],
                           Rtot[6], tnpbsa[j], biCoefMat);
        for (m = 0; m < 4; m++) {
          s = sigCoef * meanPerCond[((ixstart << 2) + l) + 24 * j];

          /* To replace normlike in the function PDF; while normlike returns */
          /* negated log probabilities, this function returns log probabilities as */
          /* they are. */
          /* -------------------------------------------------------------------------- */
          z = (mfiAdjMean[((ixstart << 2) + l) + 24 * (m + (j << 2))] - MFI) / s;
          logSqrErrMat[((ixstart << 2) + l) + 24 * ((j << 2) + m)] = -0.5 * (z *
            z) - log(2.5066282746310002 * s);
        }
      }
    }
  }

  ix = -1;
  iy = -1;
  for (i = 0; i < 8; i++) {
    ixstart = ix + 1;
    ix++;
    if (!rtIsNaN(logSqrErrMat[ixstart])) {
      s = logSqrErrMat[ixstart];
    } else {
      s = 0.0;
    }

    for (ixstart = 0; ixstart < 23; ixstart++) {
      ix++;
      if (!rtIsNaN(logSqrErrMat[ix])) {
        s += logSqrErrMat[ix];
      }
    }

    iy++;
    y[iy] = s;
  }

  logSqrErr = 0.0;
  for (ixstart = 0; ixstart < 8; ixstart++) {
    if (!rtIsNaN(y[ixstart])) {
      logSqrErr += y[ixstart];
    }
  }

  return logSqrErr;
}

/*
 * File trailer for NormalError.c
 *
 * [EOF]
 */
