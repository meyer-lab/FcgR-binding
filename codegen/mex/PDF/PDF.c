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
#include "Error.h"
#include "PDF_data.h"

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 8, "PDF",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\PDF.m" };

static emlrtBCInfo emlrtBCI = { -1, -1, 28, 61, "mfiExpPre", "PDF",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\PDF.m", 0 };

static emlrtBCInfo b_emlrtBCI = { -1, -1, 28, 63, "mfiExpPre", "PDF",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\PDF.m", 0 };

/* Function Definitions */
real_T PDF(const emlrtStack *sp, const real_T x[7], const real_T kd[24], const
           real_T mfiAdjMean4[96], const real_T mfiAdjMean26[96], const real_T
           v[2], const real_T biCoefMat[676], const real_T tnpbsa[2], const
           real_T meanPerCond[48], const real_T stdPerCond[48])
{
  real_T logprob;
  real_T b_x[7];
  int32_T ixstart;
  int32_T mfiExpPre_size[2];
  real_T mfiExpPre_data[48];
  int32_T mfiExp_size[2];
  real_T mfiExp_data[192];
  real_T s;
  real_T logprobMat[48];
  int32_T j;
  int32_T k;
  int32_T l;
  int32_T ix;
  real_T y[8];
  int32_T iy;
  int32_T i;
  emlrtStack st;
  st.prev = sp;
  st.tls = sp->tls;

  /* Find residuals for the model granted current parameters */
  /* mfiExpPre is a 6x8 matrix which includes the predicted value by the */
  /* given parameter fit for each combination of FcgR, IgG, and valency. It */
  /* is the concatenation of matrices mfiExpPre4 and mfiExpPre26; see */
  /* Error.m for their definiton */
  for (ixstart = 0; ixstart < 7; ixstart++) {
    b_x[ixstart] = x[ixstart];
  }

  st.site = &emlrtRSI;
  Error(&st, b_x, kd, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa, &s,
        mfiExp_data, mfiExp_size, mfiExpPre_data, mfiExpPre_size);

  /* Check to see that for the parameter fit there exist expected values */
  /* for the data (see Error.m lines 23 through 28) */
  if ((mfiExpPre_size[0] == 0) || (mfiExpPre_size[1] == 0)) {
    logprob = rtMinusInf;
  } else {
    /* Create a matrix which includes the log probability of the model being */
    /* chosen for each combination of data from one FcgR, one IgG, and one */
    /* valency */
    memset(&logprobMat[0], 0, 48U * sizeof(real_T));
    j = 0;
    while (j < 6) {
      k = 0;
      while (k < 4) {
        l = 0;
        while (l < 2) {
          /*                  logprobMat(j,4*(l-1)+k) = normlike([meanPerCond(4*(j-1)+k,l), ...  */
          /*                      stdPerCond(4*(j-1)+k,l)],mfiExpPre(j,4*(l-1)+k)); */
          ixstart = 1 + j;
          if (!(ixstart <= mfiExpPre_size[0])) {
            emlrtDynamicBoundsCheckR2012b(ixstart, 1, mfiExpPre_size[0],
              &emlrtBCI, sp);
          }

          ix = ((l << 2) + k) + 1;
          if (!(ix <= mfiExpPre_size[1])) {
            emlrtDynamicBoundsCheckR2012b(ix, 1, mfiExpPre_size[1], &b_emlrtBCI,
              sp);
          }

          s = mfiExpPre_data[(ixstart + mfiExpPre_size[0] * (ix - 1)) - 1];
          if (stdPerCond[((j << 2) + k) + 24 * l] > 0.0) {
            s = (s - meanPerCond[((j << 2) + k) + 24 * l]) / stdPerCond[((j << 2)
              + k) + 24 * l];
            s = muDoubleScalarExp(-0.5 * s * s) / (2.5066282746310002 *
              stdPerCond[((j << 2) + k) + 24 * l]);
          } else {
            s = rtNaN;
          }

          logprobMat[j + 6 * ((l << 2) + k)] = s;
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

    /* Sum up negative log probabilities and negate */
    ix = 0;
    iy = -1;
    for (i = 0; i < 8; i++) {
      ixstart = ix;
      ix++;
      s = logprobMat[ixstart];
      for (k = 0; k < 5; k++) {
        ix++;
        s += logprobMat[ix - 1];
      }

      iy++;
      y[iy] = s;
    }

    s = y[0];
    for (k = 0; k < 7; k++) {
      s += y[k + 1];
    }

    logprob = -s;
  }

  return logprob;
}

/* End of code generation (PDF.c) */
