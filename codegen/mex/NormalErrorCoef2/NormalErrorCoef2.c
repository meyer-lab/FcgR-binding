/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef2.c
 *
 * Code generation for function 'NormalErrorCoef2'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef2.h"
#include "error.h"
#include "StoneMod.h"
#include "NormalErrorCoef2_data.h"

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 15, "NormalErrorCoef2",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m" };

static emlrtRSInfo b_emlrtRSI = { 16, "NormalErrorCoef2",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m" };

static emlrtRSInfo c_emlrtRSI = { 21, "NormalErrorCoef2",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m" };

static emlrtRSInfo d_emlrtRSI = { 26, "NormalErrorCoef2",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m" };

static emlrtRSInfo e_emlrtRSI = { 13, "log10",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\elfun\\log10.m"
};

static emlrtRSInfo s_emlrtRSI = { 34, "NormalErrorCoef2",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m" };

static emlrtRSInfo u_emlrtRSI = { 13, "log",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\elfun\\log.m" };

static emlrtRSInfo v_emlrtRSI = { 7, "nansum",
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

static emlrtBCInfo d_emlrtBCI = { 1, 6, 13, 24, "KdMat", "NormalErrorCoef2",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m", 0 };

static emlrtDCInfo emlrtDCI = { 13, 24, "NormalErrorCoef2",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m", 1 };

/* Function Definitions */
real_T NormalErrorCoef2(const emlrtStack *sp, const real_T Rtot[12], const
  real_T KdMat[60], const real_T mfiAdjMean[192], const real_T tnpbsa[2], const
  real_T meanPerCond[48], const real_T biCoefMat[900], real_T whichR)
{
  real_T logSqrErr;
  real_T sigCoef;
  real_T logSqrErrMat[192];
  int32_T j;
  real_T c;
  int32_T k;
  real_T y[8];
  int32_T ix;
  int32_T iy;
  int32_T i;
  int32_T ixstart;
  real_T Kx;
  real_T s;
  real_T MFI;
  int32_T l;
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
  sigCoef = muDoubleScalarPower(10.0, Rtot[6]);
  memset(&logSqrErrMat[0], 0, 192U * sizeof(real_T));
  j = 0;
  while (j < 2) {
    covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 0, 1);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 1);
    c = muDoubleScalarPower(10.0, Rtot[2 + j]);
    k = 0;
    while (k < 4) {
      covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 1, 1);
      covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 2);
      if (whichR != (int32_T)muDoubleScalarFloor(whichR)) {
        emlrtIntegerCheckR2012b(whichR, &emlrtDCI, sp);
      }

      ixstart = (int32_T)whichR;
      if (!((ixstart >= 1) && (ixstart <= 6))) {
        emlrtDynamicBoundsCheckR2012b(ixstart, 1, 6, &d_emlrtBCI, sp);
      }

      Kx = KdMat[((int32_T)whichR + 6 * k) - 1] * muDoubleScalarPower(10.0,
        Rtot[1]);
      st.site = &emlrtRSI;
      if (Kx < 0.0) {
        b_st.site = &e_emlrtRSI;
        error(&b_st);
      }

      st.site = &b_emlrtRSI;
      MFI = c * StoneMod(&st, Rtot[0], KdMat[((int32_T)whichR + 6 * k) - 1],
                         Rtot[4 + j], muDoubleScalarLog10(Kx), tnpbsa[j],
                         biCoefMat);
      l = 0;
      while (l < 4) {
        covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 2, 1);
        covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 3);
        st.site = &c_emlrtRSI;
        s = sigCoef * meanPerCond[((((int32_T)whichR - 1) << 2) + k) + 24 * j];
        covrtLogFcn(&emlrtCoverageInstance, 0U, 1);
        covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 5);

        /* -------------------------------------------------------------------------- */
        /* To replace normlike in the function PDF; while normlike returns */
        /* negated log probabilities, this function returns log probabilities as */
        /* they are. */
        z = (mfiAdjMean[((((int32_T)whichR - 1) << 2) + k) + 24 * (l + (j << 2))]
             - MFI) / s;
        b_st.site = &s_emlrtRSI;
        b_st.site = &s_emlrtRSI;
        b_st.site = &s_emlrtRSI;
        s *= 2.5066282746310002;
        if (s < 0.0) {
          c_st.site = &u_emlrtRSI;
          b_error(&c_st);
        }

        logSqrErrMat[((((int32_T)whichR - 1) << 2) + k) + 24 * ((j << 2) + l)] =
          -0.5 * (z * z) - muDoubleScalarLog(s);
        l++;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }

      covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 2, 0);
      k++;
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
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 4);
  st.site = &d_emlrtRSI;
  b_st.site = &v_emlrtRSI;
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

    for (k = 0; k < 23; k++) {
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
  for (k = 0; k < 8; k++) {
    if (!muDoubleScalarIsNaN(y[k])) {
      logSqrErr += y[k];
    }
  }

  return logSqrErr;
}

/* End of code generation (NormalErrorCoef2.c) */
