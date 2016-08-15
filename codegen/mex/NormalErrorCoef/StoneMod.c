/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * StoneMod.c
 *
 * Code generation for function 'StoneMod'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef.h"
#include "StoneMod.h"
#include "power.h"
#include "NormalErrorCoef_data.h"

/* Variable Definitions */
static emlrtRSInfo f_emlrtRSI = { 15, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m" };

static emlrtRSInfo g_emlrtRSI = { 18, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m" };

static emlrtRSInfo h_emlrtRSI = { 29, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m" };

static emlrtRSInfo i_emlrtRSI = { 31, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m" };

static emlrtRSInfo j_emlrtRSI = { 32, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m" };

static emlrtRSInfo k_emlrtRSI = { 46, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m" };

static emlrtRSInfo l_emlrtRSI = { 21, "colon",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\ops\\colon.m" };

static emlrtRSInfo r_emlrtRSI = { 9, "sum",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\datafun\\sum.m"
};

static emlrtRTEInfo b_emlrtRTEI = { 48, 9, "sumprod",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\datafun\\private\\sumprod.m"
};

static emlrtRTEInfo c_emlrtRTEI = { 20, 15, "sumprod",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\datafun\\private\\sumprod.m"
};

static emlrtECInfo emlrtECI = { 2, 18, 13, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m" };

static emlrtBCInfo d_emlrtBCI = { 1, 30, 14, 31, "biCoefMat", "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m", 0 };

static emlrtDCInfo emlrtDCI = { 14, 31, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m", 1 };

static emlrtBCInfo e_emlrtBCI = { 1, 30, 14, 27, "biCoefMat", "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m", 0 };

static emlrtDCInfo b_emlrtDCI = { 14, 27, "StoneMod",
  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m", 1 };

/* Function Definitions */
real_T StoneMod(const emlrtStack *sp, real_T logR, real_T Kd, real_T v, real_T
                logKx, real_T L0, const real_T biCoefMat[900])
{
  real_T L;
  real_T Kx;
  real_T R;
  int32_T loop_ub;
  int32_T nm1d2;
  int32_T biCoefVec_size[2];
  real_T biCoefVec_data[30];
  real_T viLikdi;
  real_T a;
  real_T b;
  real_T x;
  real_T bVal;
  real_T cVal;
  real_T c;
  int32_T ndbl;
  int32_T apnd;
  int32_T cdiff;
  real_T y_data[30];
  real_T b_y_data[30];
  int32_T y_size[2];
  int32_T b_y_size[2];
  int32_T biCoefVec[2];
  int32_T y[2];
  int32_T b_biCoefVec[2];
  int32_T b_b[2];
  boolean_T p;
  boolean_T b_p;
  int32_T exitg1;
  emlrtStack st;
  emlrtStack b_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  covrtLogFcn(&emlrtCoverageInstance, 1U, 0);
  covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 0);

  /* Returns the number of mutlivalent ligand bound to a cell with 10^logR */
  /* receptors, granted each epitope of the ligand binds to the receptor */
  /* kind in question with dissociation constant Kd and cross-links with */
  /* other receptors with crosslinking constant Kx = 10^logKx. All */
  /* equations derived from Stone et al. (2001). Assumed that ligand is at */
  /* saturating concentration L0 = 7e-8 M, which is as it is (approximately) */
  /* for TNP-4-BSA in Lux et al. (2013). */
  Kx = muDoubleScalarPower(10.0, logKx);
  R = muDoubleScalarPower(10.0, logR);

  /* Vector of binomial coefficients */
  if (1.0 > v) {
    loop_ub = 0;
  } else {
    if (v != (int32_T)muDoubleScalarFloor(v)) {
      emlrtIntegerCheckR2012b(v, &b_emlrtDCI, sp);
    }

    loop_ub = (int32_T)v;
    if (!((loop_ub >= 1) && (loop_ub <= 30))) {
      emlrtDynamicBoundsCheckR2012b(loop_ub, 1, 30, &e_emlrtBCI, sp);
    }
  }

  if (v != (int32_T)muDoubleScalarFloor(v)) {
    emlrtIntegerCheckR2012b(v, &emlrtDCI, sp);
  }

  nm1d2 = (int32_T)v;
  if (!((nm1d2 >= 1) && (nm1d2 <= 30))) {
    emlrtDynamicBoundsCheckR2012b(nm1d2, 1, 30, &d_emlrtBCI, sp);
  }

  biCoefVec_size[0] = 1;
  biCoefVec_size[1] = loop_ub;
  for (nm1d2 = 0; nm1d2 < loop_ub; nm1d2++) {
    biCoefVec_data[nm1d2] = biCoefMat[nm1d2 + 30 * ((int32_T)v - 1)];
  }

  st.site = &f_emlrtRSI;
  covrtLogFcn(&emlrtCoverageInstance, 1U, 1);
  covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 1);

  /* -------------------------------------------------------------------------- */
  /* %%This function returns the point at which function fun equals zero */
  /* %%using the bisection algorithm. The closest a and b will converge to */
  /* %%in the algorithm is a distance 1e-12 apart. */
  viLikdi = v * L0 / Kd;
  a = -20.0;
  b_st.site = &h_emlrtRSI;
  b = muDoubleScalarLog10(R);
  b_st.site = &i_emlrtRSI;
  covrtLogFcn(&emlrtCoverageInstance, 1U, 2);
  covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 7);

  /* -------------------------------------------------------------------------- */
  x = muDoubleScalarPower(10.0, b);
  bVal = R - x * (1.0 + viLikdi * muDoubleScalarPower(1.0 + Kx * x, v - 1.0));
  b_st.site = &j_emlrtRSI;
  covrtLogFcn(&emlrtCoverageInstance, 1U, 2);
  covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 7);

  /* -------------------------------------------------------------------------- */
  cVal = R - 1.0000000000000001E-20 * (1.0 + viLikdi * muDoubleScalarPower(1.0 +
    Kx * 1.0000000000000001E-20, v - 1.0));

  /*  Is there no root within the interval? */
  if (covrtLogIf(&emlrtCoverageInstance, 1U, 0U, 0, bVal * cVal > 0.0)) {
    covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 2);
    c = 1000.0;
  } else {
    covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 3);

    /* In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin */
    /* with; only implemented for MATLAB Coder */
    c = 1000.0;

    /* Commence algorithm */
    while ((b - a > 0.0001) && (muDoubleScalarAbs(cVal) > 0.0001)) {
      covrtLogWhile(&emlrtCoverageInstance, 1U, 0U, 0, true);
      covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 4);
      c = (a + b) / 2.0;
      b_st.site = &k_emlrtRSI;
      covrtLogFcn(&emlrtCoverageInstance, 1U, 2);
      covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 7);

      /* -------------------------------------------------------------------------- */
      x = muDoubleScalarPower(10.0, c);
      cVal = R - x * (1.0 + viLikdi * muDoubleScalarPower(1.0 + Kx * x, v - 1.0));
      if (covrtLogIf(&emlrtCoverageInstance, 1U, 0U, 1, cVal * bVal >= 0.0)) {
        covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 5);
        b = c;
        bVal = cVal;
      } else {
        covrtLogBasicBlock(&emlrtCoverageInstance, 1U, 6);
        a = c;
      }

      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(&st);
      }
    }

    covrtLogWhile(&emlrtCoverageInstance, 1U, 0U, 0, false);
  }

  /* Calculate L, according to equations 1 and 7 */
  st.site = &g_emlrtRSI;
  b_st.site = &l_emlrtRSI;
  ndbl = (int32_T)muDoubleScalarFloor((v - 1.0) + 0.5);
  apnd = ndbl + 1;
  cdiff = (ndbl - (int32_T)v) + 1;
  if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * (real_T)(int32_T)v) {
    ndbl++;
    apnd = (int32_T)v;
  } else if (cdiff > 0) {
    apnd = ndbl;
  } else {
    ndbl++;
  }

  if (ndbl > 0) {
    y_data[0] = 1.0;
    if (ndbl > 1) {
      y_data[ndbl - 1] = apnd;
      nm1d2 = (ndbl - 1) / 2;
      for (cdiff = 1; cdiff < nm1d2; cdiff++) {
        y_data[cdiff] = 1.0 + (real_T)cdiff;
        y_data[(ndbl - cdiff) - 1] = apnd - cdiff;
      }

      if (nm1d2 << 1 == ndbl - 1) {
        y_data[nm1d2] = (1.0 + (real_T)apnd) / 2.0;
      } else {
        y_data[nm1d2] = 1.0 + (real_T)nm1d2;
        y_data[nm1d2 + 1] = apnd - nm1d2;
      }
    }
  }

  y_size[0] = 1;
  y_size[1] = ndbl;
  for (nm1d2 = 0; nm1d2 < ndbl; nm1d2++) {
    b_y_data[nm1d2] = y_data[nm1d2] - 1.0;
  }

  st.site = &g_emlrtRSI;
  power(&st, Kx, b_y_data, y_size, y_data, b_y_size);
  for (nm1d2 = 0; nm1d2 < 2; nm1d2++) {
    biCoefVec[nm1d2] = biCoefVec_size[nm1d2];
    y[nm1d2] = b_y_size[nm1d2];
  }

  if ((biCoefVec[0] != y[0]) || (biCoefVec[1] != y[1])) {
    emlrtSizeEqCheckNDR2012b(&biCoefVec[0], &y[0], &emlrtECI, sp);
  }

  biCoefVec_size[0] = 1;
  for (nm1d2 = 0; nm1d2 < loop_ub; nm1d2++) {
    biCoefVec_data[nm1d2] *= y_data[nm1d2];
  }

  st.site = &g_emlrtRSI;
  b_st.site = &l_emlrtRSI;
  ndbl = (int32_T)muDoubleScalarFloor((v - 1.0) + 0.5);
  apnd = ndbl + 1;
  cdiff = (ndbl - (int32_T)v) + 1;
  if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * (real_T)(int32_T)v) {
    ndbl++;
    apnd = (int32_T)v;
  } else if (cdiff > 0) {
    apnd = ndbl;
  } else {
    ndbl++;
  }

  b_y_size[0] = 1;
  b_y_size[1] = ndbl;
  if (ndbl > 0) {
    y_data[0] = 1.0;
    if (ndbl > 1) {
      y_data[ndbl - 1] = apnd;
      nm1d2 = (ndbl - 1) / 2;
      for (cdiff = 1; cdiff < nm1d2; cdiff++) {
        y_data[cdiff] = 1.0 + (real_T)cdiff;
        y_data[(ndbl - cdiff) - 1] = apnd - cdiff;
      }

      if (nm1d2 << 1 == ndbl - 1) {
        y_data[nm1d2] = (1.0 + (real_T)apnd) / 2.0;
      } else {
        y_data[nm1d2] = 1.0 + (real_T)nm1d2;
        y_data[nm1d2 + 1] = apnd - nm1d2;
      }
    }
  }

  x = L0 / Kd;
  st.site = &g_emlrtRSI;
  power(&st, muDoubleScalarPower(10.0, c), y_data, b_y_size, b_y_data, y_size);
  y_size[0] = 1;
  cdiff = y_size[1];
  for (nm1d2 = 0; nm1d2 < cdiff; nm1d2++) {
    b_y_data[nm1d2] *= x;
  }

  for (nm1d2 = 0; nm1d2 < 2; nm1d2++) {
    b_biCoefVec[nm1d2] = biCoefVec_size[nm1d2];
    b_b[nm1d2] = y_size[nm1d2];
  }

  if ((b_biCoefVec[0] != b_b[0]) || (b_biCoefVec[1] != b_b[1])) {
    emlrtSizeEqCheckNDR2012b(&b_biCoefVec[0], &b_b[0], &emlrtECI, sp);
  }

  st.site = &g_emlrtRSI;
  biCoefVec_size[0] = 1;
  for (nm1d2 = 0; nm1d2 < loop_ub; nm1d2++) {
    biCoefVec_data[nm1d2] *= b_y_data[nm1d2];
  }

  b_st.site = &r_emlrtRSI;
  if ((loop_ub == 1) || (loop_ub != 1)) {
    p = true;
  } else {
    p = false;
  }

  if (p) {
  } else {
    emlrtErrorWithMessageIdR2012b(&b_st, &c_emlrtRTEI,
      "Coder:toolbox:autoDimIncompatibility", 0);
  }

  p = false;
  b_p = false;
  cdiff = 0;
  do {
    exitg1 = 0;
    if (cdiff < 2) {
      if (biCoefVec_size[cdiff] != 0) {
        exitg1 = 1;
      } else {
        cdiff++;
      }
    } else {
      b_p = true;
      exitg1 = 1;
    }
  } while (exitg1 == 0);

  if (!b_p) {
  } else {
    p = true;
  }

  if (!p) {
  } else {
    emlrtErrorWithMessageIdR2012b(&b_st, &b_emlrtRTEI,
      "Coder:toolbox:UnsupportedSpecialEmpty", 0);
  }

  if (loop_ub == 0) {
    L = 0.0;
  } else {
    L = biCoefVec_data[0];
    for (cdiff = 2; cdiff <= loop_ub; cdiff++) {
      L += biCoefVec_data[cdiff - 1];
    }
  }

  return L;
}

/* End of code generation (StoneMod.c) */
