/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PROPRND.c
 *
 * Code generation for function 'PROPRND'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "error.h"
#include "PROPRND_data.h"

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 11, "PROPRND",
  "C:\\Users\\mitadm\\Downloads\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\"
  "PROPRND.m" };

static emlrtRSInfo b_emlrtRSI = { 20, "PROPRND",
  "C:\\Users\\mitadm\\Downloads\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\"
  "PROPRND.m" };

static emlrtRSInfo c_emlrtRSI = { 29, "PROPRND",
  "C:\\Users\\mitadm\\Downloads\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\"
  "PROPRND.m" };

static emlrtRSInfo f_emlrtRSI = { 52, "PROPRND",
  "C:\\Users\\mitadm\\Downloads\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\"
  "PROPRND.m" };

static emlrtRSInfo g_emlrtRSI = { 61, "PROPRND",
  "C:\\Users\\mitadm\\Downloads\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\"
  "PROPRND.m" };

static emlrtRSInfo h_emlrtRSI = { 62, "PROPRND",
  "C:\\Users\\mitadm\\Downloads\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\"
  "PROPRND.m" };

static emlrtRSInfo i_emlrtRSI = { 10, "exprnd",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\stats\\eml\\exprnd.m" };

static emlrtRSInfo j_emlrtRSI = { 1, "rnd",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\eml\\+coder\\+internal\\rnd.p"
};

static emlrtRSInfo k_emlrtRSI = { 1, "exprnd",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\eml\\+coder\\+internal\\private\\exprnd.p"
};

static emlrtRSInfo l_emlrtRSI = { 13, "log",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\elfun\\log.m" };

static emlrtRSInfo m_emlrtRSI = { 61, "randi",
  "C:\\Program Files\\MATLAB\\R2016a\\toolbox\\eml\\lib\\matlab\\randfun\\randi.m"
};

/* Function Declarations */
static real_T twotailexprnd(const emlrtStack *sp, real_T inversestd);

/* Function Definitions */
static real_T twotailexprnd(const emlrtStack *sp, real_T inversestd)
{
  real_T val;
  real_T x;
  real_T temp;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  emlrtStack e_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  e_st.prev = &d_st;
  e_st.tls = d_st.tls;
  covrtLogFcn(&emlrtCoverageInstance, 0U, 1);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 17);

  /* -------------------------------------------------------------------------- */
  /*  inversestd represents the reciprocal of the standard deviation of the */
  /*  corresponding exponential distribution, which happens to be equal to */
  /*  the mean of the corresponding exponential distribution */
  st.site = &g_emlrtRSI;
  b_st.site = &i_emlrtRSI;
  c_st.site = &j_emlrtRSI;
  d_st.site = &k_emlrtRSI;
  emlrtRandu(&x, 1);
  d_st.site = &k_emlrtRSI;
  if (x < 0.0) {
    e_st.site = &l_emlrtRSI;
    error(&e_st);
  }

  val = -inversestd * muDoubleScalarLog(x);
  if (inversestd < 0.0) {
    val = rtNaN;
  }

  st.site = &h_emlrtRSI;
  b_st.site = &m_emlrtRSI;
  emlrtRandu(&temp, 1);
  if (covrtLogIf(&emlrtCoverageInstance, 0U, 0U, 0, 1.0 + muDoubleScalarFloor
                 (temp * 2.0) == 1.0)) {
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 18);
    val = -val;
  }

  return val;
}

void PROPRND(const emlrtStack *sp, const real_T current[12], real_T lbR, real_T
             ubR, real_T lbKx, real_T ubKx, real_T lbc, real_T ubc, real_T lbv,
             real_T ubv, real_T lbsigma, real_T ubsigma, real_T stdR, real_T
             stdKx, real_T stdc, real_T stdsigma, real_T next[12])
{
  real_T b_lbR[12];
  int32_T i0;
  int32_T j;
  real_T NEXT;
  real_T NEXT10;
  real_T NEXT11;
  real_T r;
  emlrtStack st;
  st.prev = sp;
  st.tls = sp->tls;
  covrtLogFcn(&emlrtCoverageInstance, 0U, 0);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 0);

  /*  Preset next below all minimum thresholds */
  for (i0 = 0; i0 < 6; i0++) {
    b_lbR[i0] = lbR;
  }

  b_lbR[6] = lbKx;
  for (i0 = 0; i0 < 2; i0++) {
    b_lbR[i0 + 7] = lbc;
  }

  b_lbR[9] = 1.0;
  b_lbR[10] = 1.0;
  b_lbR[11] = lbsigma;
  for (i0 = 0; i0 < 12; i0++) {
    next[i0] = b_lbR[i0] - 1.0;
  }

  /*  Generate new logR values */
  j = 0;
  while (j < 6) {
    covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 0, 1);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 1);
    NEXT = next[j];
    while ((NEXT < lbR) || (ubR < NEXT)) {
      covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 0, true);
      covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 2);
      st.site = &emlrtRSI;
      NEXT = current[j] + twotailexprnd(&st, stdR);
      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(sp);
      }
    }

    covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 0, false);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 3);
    next[j] = NEXT;
    j++;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 0, 0);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 4);

  /* Generate new logKx value */
  NEXT = next[6];
  while ((NEXT < lbKx) || (ubKx < NEXT)) {
    covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 1, true);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 5);
    st.site = &b_emlrtRSI;
    NEXT = current[6] + twotailexprnd(&st, stdKx);
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 1, false);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 6);
  next[6] = NEXT;

  /* Generate new common logs of conversion coefficients */
  j = 7;
  while (j - 7 < 2) {
    covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 1, 1);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 7);
    NEXT = next[j];
    while ((NEXT < lbc) || (ubc < NEXT)) {
      covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 2, true);
      covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 8);
      st.site = &c_emlrtRSI;
      NEXT = current[j] + twotailexprnd(&st, stdc);
      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(sp);
      }
    }

    covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 2, false);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 9);
    next[j] = NEXT;
    j++;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  covrtLogFor(&emlrtCoverageInstance, 0U, 0U, 1, 0);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 10);

  /* Generate new avidities     */
  NEXT10 = next[9];
  NEXT11 = next[10];
  while ((NEXT10 < lbv) || (ubv < NEXT10)) {
    covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 3, true);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 11);
    emlrtRandu(&r, 1);
    NEXT10 = (current[9] + (1.0 + muDoubleScalarFloor(r * 3.0))) - 2.0;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 3, false);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 12);
  next[9] = NEXT10;
  while ((NEXT11 < lbv) || (ubv < NEXT11)) {
    covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 4, true);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 13);
    emlrtRandu(&r, 1);
    NEXT11 = (current[10] + (1.0 + muDoubleScalarFloor(r * 3.0))) - 2.0;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 4, false);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 14);
  next[10] = NEXT11;

  /*  Generate next standard deviation coefficient */
  NEXT = next[11];
  while ((NEXT < lbsigma) || (ubsigma < NEXT)) {
    covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 5, true);
    covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 15);
    st.site = &f_emlrtRSI;
    NEXT = current[11] + twotailexprnd(&st, stdsigma);
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  covrtLogWhile(&emlrtCoverageInstance, 0U, 0U, 5, false);
  covrtLogBasicBlock(&emlrtCoverageInstance, 0U, 16);
  next[11] = NEXT;
}

/* End of code generation (PROPRND.c) */
