/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PDF.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 22-Jun-2016 09:56:36
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "Error.h"

/* Function Definitions */

/*
 * Find residuals for the model granted current parameters
 * Arguments    : const double x[7]
 *                const double kd[24]
 *                const double mfiAdjMean4[96]
 *                const double mfiAdjMean26[96]
 *                const double v[2]
 *                const double biCoefMat[676]
 *                const double tnpbsa[2]
 *                const double meanPerCond[48]
 *                const double stdPerCond[48]
 * Return Type  : double
 */
double PDF(const double x[7], const double kd[24], const double mfiAdjMean4[96],
           const double mfiAdjMean26[96], const double v[2], const double
           biCoefMat[676], const double tnpbsa[2], const double meanPerCond[48],
           const double stdPerCond[48])
{
  double logprob;
  double b_x[7];
  int ixstart;
  int mfiExpPre_size[2];
  double mfiExpPre_data[48];
  int mfiExp_size[2];
  double mfiExp_data[192];
  double s;
  double logprobMat[48];
  int j;
  int l;
  double y[8];
  int ix;
  int iy;
  int i;

  /* mfiExpPre is a 6x8 matrix which includes the predicted value by the */
  /* given parameter fit for each combination of FcgR, IgG, and valency. It */
  /* is the concatenation of matrices mfiExpPre4 and mfiExpPre26; see */
  /* Error.m for their definiton */
  for (ixstart = 0; ixstart < 7; ixstart++) {
    b_x[ixstart] = x[ixstart];
  }

  Error(b_x, kd, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa, &s,
        mfiExp_data, mfiExp_size, mfiExpPre_data, mfiExpPre_size);

  /* Check to see that for the parameter fit there exist expected values */
  /* for the data (see Error.m lines 23 through 28) */
  if ((mfiExpPre_size[0] == 0) || (mfiExpPre_size[1] == 0)) {
    logprob = rtMinusInf;
  } else {
    /* Create a matrix which includes the log probability of the model being */
    /* chosen for each combination of data from one FcgR, one IgG, and one */
    /* valency */
    memset(&logprobMat[0], 0, 48U * sizeof(double));
    for (j = 0; j < 6; j++) {
      for (ixstart = 0; ixstart < 4; ixstart++) {
        for (l = 0; l < 2; l++) {
          /*                  logprobMat(j,4*(l-1)+k) = normlike([meanPerCond(4*(j-1)+k,l), ...  */
          /*                      stdPerCond(4*(j-1)+k,l)],mfiExpPre(j,4*(l-1)+k)); */
          if (stdPerCond[((j << 2) + ixstart) + 24 * l] > 0.0) {
            s = (mfiExpPre_data[j + mfiExpPre_size[0] * ((l << 2) + ixstart)] -
                 meanPerCond[((j << 2) + ixstart) + 24 * l]) / stdPerCond[((j <<
              2) + ixstart) + 24 * l];
            s = exp(-0.5 * s * s) / (2.5066282746310002 * stdPerCond[((j << 2) +
              ixstart) + 24 * l]);
          } else {
            s = rtNaN;
          }

          logprobMat[j + 6 * ((l << 2) + ixstart)] = s;
        }
      }
    }

    /* Sum up negative log probabilities and negate */
    ix = 0;
    iy = -1;
    for (i = 0; i < 8; i++) {
      ixstart = ix;
      ix++;
      s = logprobMat[ixstart];
      for (ixstart = 0; ixstart < 5; ixstart++) {
        ix++;
        s += logprobMat[ix - 1];
      }

      iy++;
      y[iy] = s;
    }

    s = y[0];
    for (ixstart = 0; ixstart < 7; ixstart++) {
      s += y[ixstart + 1];
    }

    logprob = -s;
  }

  return logprob;
}

/*
 * File trailer for PDF.c
 *
 * [EOF]
 */
