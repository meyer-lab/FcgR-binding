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

static emlrtRSInfo r_emlrtRSI = { 36, "PDF",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\PDF.m" };

static emlrtRSInfo t_emlrtRSI = { 13, "log",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\elfun\\log.m" };

/* Function Definitions */
real_T PDF(const emlrtStack *sp, const real_T x[7], const real_T kd[24], const
           real_T mfiAdjMean[192], const real_T v[2], const real_T biCoefMat[676],
           const real_T tnpbsa[2], const real_T meanPerCond[48], const real_T
           stdPerCond[48])
{
  real_T logprob;
  real_T b_x[7];
  int32_T ixstart;
  real_T mfiExpPre[48];
  int32_T unusedU1_size[2];
  real_T unusedU1_data[192];
  real_T mtmp;
  boolean_T guard1 = false;
  int32_T ix;
  boolean_T exitg1;
  int32_T j;
  int32_T k;
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
  for (ixstart = 0; ixstart < 7; ixstart++) {
    b_x[ixstart] = x[ixstart];
  }

  st.site = &emlrtRSI;
  Error(&st, b_x, kd, mfiAdjMean, v, biCoefMat, tnpbsa, &mtmp, unusedU1_data,
        unusedU1_size, mfiExpPre);

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
      while ((!exitg1) && (ix < 8)) {
        ixstart = ix;
        if (!muDoubleScalarIsNaN(x[ix - 1])) {
          mtmp = x[ix - 1];
          exitg1 = true;
        } else {
          ix++;
        }
      }
    }

    if (ixstart < 7) {
      while (ixstart + 1 < 8) {
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
        k = 0;
        while (k < 4) {
          l = 0;
          while (l < 2) {
            st.site = &b_emlrtRSI;

            /* -------------------------------------------------------------------------- */
            /* To replace normlike in the function PDF; while normlike returns */
            /* negated log probabilities, this function returns log probabilities as */
            /* they are. */
            b_st.site = &r_emlrtRSI;
            b_st.site = &r_emlrtRSI;
            b_st.site = &r_emlrtRSI;
            mtmp = 2.5066282746310002 * stdPerCond[((j << 2) + k) + 24 * l];
            if (mtmp < 0.0) {
              c_st.site = &t_emlrtRSI;
              b_error(&c_st);
            }

            logprob += -0.5 * muDoubleScalarPower((mfiExpPre[j + 6 * ((l << 2) +
              k)] - meanPerCond[((j << 2) + k) + 24 * l]) / stdPerCond[((j << 2)
              + k) + 24 * l], 2.0) - muDoubleScalarLog(mtmp);
            l++;
            if (*emlrtBreakCheckR2012bFlagVar != 0) {
              emlrtBreakCheckR2012b(sp);
            }
          }

          k++;
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
