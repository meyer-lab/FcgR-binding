/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalError2.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 10-Aug-2016 17:28:35
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalError2.h"
#include "StoneMod.h"
#include "power.h"
#include "NormalError2_rtwutil.h"

/* Function Definitions */

/*
 * Arguments    : const double Rtot[7]
 *                const double KdMat[60]
 *                const double mfiAdjMean[192]
 *                const double tnpbsa[2]
 *                const double meanPerCond[48]
 *                const double biCoefMat[900]
 *                double whichR
 * Return Type  : double
 */
double NormalError2(const double Rtot[7], const double KdMat[60], const double
                    mfiAdjMean[192], const double tnpbsa[2], const double
                    meanPerCond[48], const double biCoefMat[900], double whichR)
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
  double MFI;
  int l;
  double s;
  double z;
  sigCoef = rt_powd_snf(10.0, Rtot[6]);
  memset(&logSqrErrMat[0], 0, 192U * sizeof(double));
  for (j = 0; j < 2; j++) {
    c = rt_powd_snf(10.0, Rtot[2 + j]);
    for (ixstart = 0; ixstart < 4; ixstart++) {
      MFI = c * StoneMod(Rtot[0], KdMat[((int)whichR + 6 * ixstart) - 1], Rtot[4
                         + j], Rtot[1], tnpbsa[j], biCoefMat);
      for (l = 0; l < 4; l++) {
        s = sigCoef * meanPerCond[((((int)whichR - 1) << 2) + ixstart) + 24 * j];

        /* To replace normlike in the function PDF; while normlike returns */
        /* negated log probabilities, this function returns log probabilities as */
        /* they are. */
        /* -------------------------------------------------------------------------- */
        z = (mfiAdjMean[((((int)whichR - 1) << 2) + ixstart) + 24 * (l + (j << 2))]
             - MFI) / s;
        logSqrErrMat[((((int)whichR - 1) << 2) + ixstart) + 24 * ((j << 2) + l)]
          = -0.5 * (z * z) - log(2.5066282746310002 * s);
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
 * File trailer for NormalError2.c
 *
 * [EOF]
 */
