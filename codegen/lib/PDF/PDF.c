/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PDF.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 23-Jun-2016 16:03:51
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "StoneSolver.h"
#include "PDF_rtwutil.h"

/* Function Definitions */

/*
 * Find residuals for the model granted current parameters
 * Arguments    : const double x[7]
 *                const double kd[24]
 *                const double mfiAdjMean[192]
 *                const double v[2]
 *                const double biCoefMat[676]
 *                const double tnpbsa[2]
 *                const double meanPerCond[48]
 *                const double stdPerCond[48]
 * Return Type  : double
 */
double PDF(const double x[7], const double kd[24], const double mfiAdjMean[192],
           const double v[2], const double biCoefMat[676], const double tnpbsa[2],
           const double meanPerCond[48], const double stdPerCond[48])
{
  double logprob;
  double Rtot[7];
  int k;
  double Kx;
  double mfiExpPre[48];
  int j;
  boolean_T varargin_1[48];
  boolean_T maxval[8];
  boolean_T mtmp;
  boolean_T guard1 = false;
  int ixstart;
  double b_mtmp;
  boolean_T exitg1;
  int l;
  (void)mfiAdjMean;

  /* mfiExpPre is a 6x8 matrix which includes the predicted value by the */
  /* given parameter fit for each combination of FcgR, IgG, and valency. It */
  /* is the concatenation of matrices mfiExpPre4 and mfiExpPre26; see */
  /* Error.m for their definiton */
  /*  If error is called with Rtot being a single value, assume we want to */
  /*  have constant expression across all the receptors */
  /* Convert from log scale */
  for (k = 0; k < 7; k++) {
    Rtot[k] = rt_powd_snf(10.0, x[k]);
  }

  Kx = Rtot[6];

  /* Get expected value of MFIs from Equation 7 from Stone */
  memset(&mfiExpPre[0], 0, 48U * sizeof(double));
  for (j = 0; j < 6; j++) {
    for (k = 0; k < 4; k++) {
      mfiExpPre[j + 6 * k] = StoneSolver(Rtot[j], Kx, v[0], kd[j + 6 * k],
        tnpbsa[0], biCoefMat);
      mfiExpPre[j + 6 * (4 + k)] = StoneSolver(Rtot[j], Kx, v[1], kd[j + 6 * k],
        tnpbsa[1], biCoefMat);
    }
  }

  /* Check for undefined values (errors from ReqFuncSolver) */
  for (k = 0; k < 48; k++) {
    varargin_1[k] = (mfiExpPre[k] == -1.0);
  }

  for (j = 0; j < 8; j++) {
    maxval[j] = varargin_1[6 * j];
    for (k = 0; k < 5; k++) {
      mtmp = maxval[j];
      if ((int)varargin_1[(k + 6 * j) + 1] > (int)maxval[j]) {
        mtmp = varargin_1[(k + 6 * j) + 1];
      }

      maxval[j] = mtmp;
    }
  }

  mtmp = maxval[0];
  for (k = 0; k < 7; k++) {
    if ((int)maxval[k + 1] > (int)mtmp) {
      mtmp = maxval[k + 1];
    }
  }

  if (mtmp) {
    for (k = 0; k < 48; k++) {
      mfiExpPre[k] = -1.0;
    }
  } else {
    /* Create array of expected values to calculate residuals */
    /* Error */
  }

  /* Check to see that for the parameter fit there exist expected values */
  /* for the data (see Error.m lines 23 through 28) */
  guard1 = false;
  if (mfiExpPre[0] == -1.0) {
    guard1 = true;
  } else {
    ixstart = 1;
    b_mtmp = x[0];
    if (rtIsNaN(x[0])) {
      k = 2;
      exitg1 = false;
      while ((!exitg1) && (k < 8)) {
        ixstart = k;
        if (!rtIsNaN(x[k - 1])) {
          b_mtmp = x[k - 1];
          exitg1 = true;
        } else {
          k++;
        }
      }
    }

    if (ixstart < 7) {
      while (ixstart + 1 < 8) {
        if (x[ixstart] > b_mtmp) {
          b_mtmp = x[ixstart];
        }

        ixstart++;
      }
    }

    if (b_mtmp > 8.0) {
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
