/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PDF.c
 *
 * Code generation for function 'PDF'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "error1.h"
#include "Error.h"
#include "PDF_data.h"

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 8, "PDF",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\PDF.m" };

static emlrtRSInfo b_emlrtRSI = { 24, "PDF",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\PDF.m" };

static emlrtRSInfo c_emlrtRSI = { 15, "ErrorAvidityChange",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\ErrorAvidityChange.m" };

static emlrtRSInfo s_emlrtRSI = { 36, "PDF",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\PDF.m" };

static emlrtRSInfo u_emlrtRSI = { 13, "log",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\elfun\\log.m" };

static emlrtECInfo emlrtECI = { 2, 18, 15, "ErrorAvidityChange",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\ErrorAvidityChange.m" };

/* Function Definitions */
real_T PDF(const emlrtStack *sp, const real_T x[11], const real_T kd[24], const
           real_T mfiAdjMean[192], const real_T biCoefMat[676], const real_T
           tnpbsa[2], const real_T meanPerCond[48], const real_T stdPerCond[48])
{
  real_T logprob;
  real_T dv0[2];
  int32_T ixstart;
  real_T b_x[9];
  real_T mfiExpPre[48];
  int32_T mfiExp_size[2];
  real_T mfiExp_data[192];
  real_T mtmp;
  int32_T iv0[2];
  boolean_T guard1 = false;
  int32_T ix;
  boolean_T exitg1;
  int32_T j;
  int32_T l;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;

  /* Find residuals for the model granted current parameters */
  /* mfiExpPre is a 6x8 matrix which includes the predicted value by the */
  /* given parameter fit for each combination of FcgR, IgG, and valency. It */
  /* is the concatenation of matrices mfiExpPre4 and mfiExpPre26; see */
  /* Error.m for their definiton */
  st.site = &emlrtRSI;

  /* Treats the last two elements of RtotTrue as the effective avidities of */
  /* TNP-4-BSA and TNP-26-BSA respectively (as of June 27, 2016, these are */
  /* elements 10 and 11). Runs Error.m inputting these two avidities as a */
  /* two-dimensional column vector which is passed into Error as the vector */
  /* v. */
  /*  If error is called with Rtot being a single value, assume we want to */
  /*  have constant expression across all the receptors */
  for (ixstart = 0; ixstart < 2; ixstart++) {
    dv0[ixstart] = muDoubleScalarCeil(x[9 + ixstart]);
  }

  memcpy(&b_x[0], &x[0], 9U * sizeof(real_T));
  b_st.site = &c_emlrtRSI;
  Error(&b_st, b_x, kd, mfiAdjMean, dv0, biCoefMat, tnpbsa, &mtmp, mfiExp_data,
        mfiExp_size, mfiExpPre);
  for (ixstart = 0; ixstart < 2; ixstart++) {
    iv0[ixstart] = 24 + -16 * ixstart;
  }

  if ((mfiExp_size[0] != iv0[0]) || (mfiExp_size[1] != iv0[1])) {
    emlrtSizeEqCheckNDR2012b(&mfiExp_size[0], &iv0[0], &emlrtECI, &st);
  }

  /* Check to see that for the parameter fit there exist expected values */
  /* for the data (see Error.m lines 23 through 28) */
  guard1 = false;
  if (mfiExpPre[0] == -1.0) {
    guard1 = true;
  } else {
    ixstart = 1;
    mtmp = x[0];
    if (muDoubleScalarIsNaN(x[0])) {
      ix = 2;
      exitg1 = false;
      while ((!exitg1) && (ix < 12)) {
        ixstart = ix;
        if (!muDoubleScalarIsNaN(x[ix - 1])) {
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
      j = 0;
      while (j < 6) {
        ixstart = 0;
        while (ixstart < 4) {
          l = 0;
          while (l < 2) {
            st.site = &b_emlrtRSI;

            /* -------------------------------------------------------------------------- */
            /* To replace normlike in the function PDF; while normlike returns */
            /* negated log probabilities, this function returns log probabilities as */
            /* they are. */
            b_st.site = &s_emlrtRSI;
            b_st.site = &s_emlrtRSI;
            b_st.site = &s_emlrtRSI;
            mtmp = 2.5066282746310002 * stdPerCond[((j << 2) + ixstart) + 24 * l];
            if (mtmp < 0.0) {
              c_st.site = &u_emlrtRSI;
              b_error(&c_st);
            }

            logprob += -0.5 * muDoubleScalarPower((mfiExpPre[j + 6 * ((l << 2) +
              ixstart)] - meanPerCond[((j << 2) + ixstart) + 24 * l]) /
              stdPerCond[((j << 2) + ixstart) + 24 * l], 2.0) -
              muDoubleScalarLog(mtmp);
            l++;
            if (*emlrtBreakCheckR2012bFlagVar != 0) {
              emlrtBreakCheckR2012b(sp);
            }
          }

          ixstart++;
          if (*emlrtBreakCheckR2012bFlagVar != 0) {
            emlrtBreakCheckR2012b(sp);
          }
        }

        j++;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }
    }
  }

  if (guard1) {
    logprob = rtMinusInf;
  }

  return logprob;
}

/* End of code generation (PDF.c) */
