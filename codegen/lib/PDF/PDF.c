/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PDF.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 30-Jun-2016 10:18:23
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "ErrorAvidityChange.h"
#include "PDF_rtwutil.h"

/* Function Definitions */

/*
 * Find residuals for the model granted current parameters
 * Arguments    : const double x[11]
 *                const double kd[24]
 *                const double mfiAdjMean[192]
 *                const double biCoefMat[676]
 *                const double tnpbsa[2]
 *                const double meanPerCond[48]
 *                const double stdPerCond[48]
 * Return Type  : double
 */
double PDF(const double x[11], const double kd[24], const double mfiAdjMean[192],
           const double biCoefMat[676], const double tnpbsa[2], const double
           meanPerCond[48], const double stdPerCond[48])
{
  double logprob;
  double mfiExpPre[48];
  int unusedU1_size[2];
  double unusedU1_data[192];
  double mtmp;
  boolean_T guard1 = false;
  int ixstart;
  int ix;
  boolean_T exitg1;
  int j;
  int k;
  int l;

  /* mfiExpPre is a 6x8 matrix which includes the predicted value by the */
  /* given parameter fit for each combination of FcgR, IgG, and valency. It */
  /* is the concatenation of matrices mfiExpPre4 and mfiExpPre26; see */
  /* Error.m for their definiton */
  ErrorAvidityChange(x, kd, mfiAdjMean, biCoefMat, tnpbsa, &mtmp, unusedU1_data,
                     unusedU1_size, mfiExpPre);

  /* Check to see that for the parameter fit there exist expected values */
  /* for the data (see Error.m lines 23 through 28) */
  guard1 = false;
  if (mfiExpPre[0] == -1.0) {
    guard1 = true;
  } else {
    ixstart = 1;
    mtmp = x[0];
    if (rtIsNaN(x[0])) {
      ix = 2;
      exitg1 = false;
      while ((!exitg1) && (ix < 12)) {
        ixstart = ix;
        if (!rtIsNaN(x[ix - 1])) {
          mtmp = x[ix - 1];
          exitg1 = true;
        } else {
          ix++;
        }
      }
    }

    if (ixstart < 11) {
      while (ixstart + 1 < 12) {
        if (x[ixstart] > mtmp) {
          mtmp = x[ixstart];
        }

        ixstart++;
      }
    }

    if (mtmp > 8.0) {
      guard1 = true;
    } else {
      /* Create a matrix which includes the log probability of the model being */
      /* chosen for each combination of data from one FcgR, one IgG, and one */
      /* valency */
      logprob = 0.0;
      for (j = 0; j < 6; j++) {
        for (k = 0; k < 4; k++) {
          for (l = 0; l < 2; l++) {
            /* To replace normlike in the function PDF; while normlike returns */
            /* negated log probabilities, this function returns log probabilities as */
            /* they are. */
            /* -------------------------------------------------------------------------- */
            logprob += -0.5 * rt_powd_snf((mfiExpPre[j + 6 * ((l << 2) + k)] -
              meanPerCond[((j << 2) + k) + 24 * l]) / stdPerCond[((j << 2) + k)
              + 24 * l], 2.0) - log(2.5066282746310002 * stdPerCond[((j << 2) +
              k) + 24 * l]);
          }
        }
      }
    }
  }

  if (guard1) {
    logprob = rtMinusInf;
  }

  return logprob;
}

/*
 * File trailer for PDF.c
 *
 * [EOF]
 */
