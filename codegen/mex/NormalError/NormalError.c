/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalError.c
 *
 * Code generation for function 'NormalError'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalError.h"
#include "error.h"
#include "StoneMod.h"
#include "NormalError_data.h"

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 15, "NormalError",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum2\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\NormalError.m"
};

static emlrtRSInfo b_emlrtRSI = { 20, "NormalError",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum2\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\NormalError.m"
};

static emlrtRSInfo c_emlrtRSI = { 26, "NormalError",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum2\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\NormalError.m"
};

static emlrtRSInfo q_emlrtRSI = { 34, "NormalError",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum2\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\NormalError.m"
};

static emlrtRSInfo s_emlrtRSI = { 13, "log",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\elfun\\log.m" };

static emlrtRSInfo t_emlrtRSI = { 7, "nansum",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\stats\\eml\\nansum.m" };

static emlrtBCInfo emlrtBCI = { 1, 8, 128, 13, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtBCInfo b_emlrtBCI = { 1, 192, 113, 27, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtBCInfo c_emlrtBCI = { 1, 192, 100, 23, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

/* Function Definitions */
real_T NormalError(const emlrtStack *sp, const real_T Rtot[12], const real_T
                   KdMat[60], const real_T mfiAdjMean[192], const real_T tnpbsa
                   [2], const real_T meanPerCond[48], const real_T biCoefMat[900])
{
  real_T logSqrErr;
  real_T sigCoef;
  real_T logSqrErrMat[192];
  int32_T j;
  real_T c;
  int32_T ixstart;
  real_T y[8];
  int32_T ix;
  int32_T iy;
  int32_T i;
  int32_T l;
  real_T MFI;
  real_T s;
  int32_T m;
  real_T z;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  covrtLogFcn(&emlrtCoverageInstance, 0U, 0);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 0);
  sigCoef = muDoubleScalarPower(10.0, Rtot[11]);
  memset(&logSqrErrMat[0], 0, 192U * sizeof(real_T));
  j = 0;
  while (j < 2) {
    covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 0, 1);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 1);
    c = muDoubleScalarPower(10.0, Rtot[7 + j]);
    ixstart = 0;
    while (ixstart < 6) {
      covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 1, 1);
      covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 2);
      l = 0;
      while (l < 4) {
        covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 2, 1);
        covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 3);
        st.site = &emlrtRSI;
        MFI = c * StoneMod(&st, Rtot[ixstart], KdMat[ixstart + 6 * l], Rtot[9 +
                           j], Rtot[6], tnpbsa[j], biCoefMat);
        m = 0;
        while (m < 4) {
          covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 3, 1);
          covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 4);
          st.site = &b_emlrtRSI;
          s = sigCoef * meanPerCond[((ixstart << 2) + l) + 24 * j];
          covrtLogFcn(&emlrtCoverageInstance, 0U, 1);
          covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 6);

          /* -------------------------------------------------------------------------- */
          /* To replace normlike in the function PDF; while normlike returns */
          /* negated log probabilities, this function returns log probabilities as */
          /* they are. */
          z = (mfiAdjMean[((ixstart << 2) + l) + 24 * (m + (j << 2))] - MFI) / s;
          b_st.site = &q_emlrtRSI;
          b_st.site = &q_emlrtRSI;
          b_st.site = &q_emlrtRSI;
          s *= 2.5066282746310002;
          if (s < 0.0) {
            c_st.site = &s_emlrtRSI;
            error(&c_st);
          }

          logSqrErrMat[((ixstart << 2) + l) + 24 * ((j << 2) + m)] = -0.5 * (z *
            z) - muDoubleScalarLog(s);
          m++;
          if (*emlrtBreakCheckR2012bFlagVar != 0) {
            emlrtBreakCheckR2012b(sp);
          }
        }

        covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 3, 0);
        l++;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }

      covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 2, 0);
      ixstart++;
      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(sp);
      }
    }

    covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 1, 0);
    j++;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 0, 0);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 5);
  st.site = &c_emlrtRSI;
  b_st.site = &t_emlrtRSI;
  ix = 0;
  iy = 0;
  for (i = 0; i < 8; i++) {
    ixstart = ix;
    ix++;
    if (!((ixstart + 1 >= 1) && (ixstart + 1 <= 192))) {
      emlrtDynamicBoundsCheckR2012b(ixstart + 1, 1, 192, &c_emlrtBCI, &b_st);
    }

    if (!muDoubleScalarIsNaN(logSqrErrMat[ixstart])) {
      s = logSqrErrMat[ixstart];
    } else {
      s = 0.0;
    }

    for (ixstart = 0; ixstart < 23; ixstart++) {
      ix++;
      if (!((ix >= 1) && (ix <= 192))) {
        emlrtDynamicBoundsCheckR2012b(ix, 1, 192, &b_emlrtBCI, &b_st);
      }

      if (!muDoubleScalarIsNaN(logSqrErrMat[ix - 1])) {
        s += logSqrErrMat[ix - 1];
      }
    }

    iy++;
    if (!((iy >= 1) && (iy <= 8))) {
      emlrtDynamicBoundsCheckR2012b(iy, 1, 8, &emlrtBCI, &b_st);
    }

    y[iy - 1] = s;
  }

  logSqrErr = 0.0;
  for (ixstart = 0; ixstart < 8; ixstart++) {
    if (!muDoubleScalarIsNaN(y[ixstart])) {
      logSqrErr += y[ixstart];
    }
  }

  return logSqrErr;
}

/* End of code generation (NormalError.c) */
