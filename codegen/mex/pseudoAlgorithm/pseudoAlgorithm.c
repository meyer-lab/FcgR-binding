/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * pseudoAlgorithm.c
 *
 * Code generation for function 'pseudoAlgorithm'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "pseudoAlgorithm_emxutil.h"
#include "PDF.h"
#include "PROPRND.h"
#include "randi.h"
#include "pseudoAlgorithm_data.h"

/* Variable Definitions */
static emlrtRSInfo emlrtRSI = { 6, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo b_emlrtRSI = { 7, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo c_emlrtRSI = { 11, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo d_emlrtRSI = { 17, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo e_emlrtRSI = { 22, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo f_emlrtRSI = { 23, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo g_emlrtRSI = { 28, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo h_emlrtRSI = { 41, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo i_emlrtRSI = { 42, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRSInfo j_emlrtRSI = { 47, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRTEInfo emlrtRTEI = { 1, 33, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtDCInfo emlrtDCI = { 4, 14, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 4 };

static emlrtDCInfo b_emlrtDCI = { 4, 14, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtDCInfo c_emlrtDCI = { 4, 26, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 4 };

static emlrtDCInfo d_emlrtDCI = { 4, 26, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtDCInfo e_emlrtDCI = { 5, 13, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 4 };

static emlrtDCInfo f_emlrtDCI = { 5, 13, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtDCInfo g_emlrtDCI = { 5, 24, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 4 };

static emlrtDCInfo h_emlrtDCI = { 5, 24, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtECInfo emlrtECI = { 1, 6, 15, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtECInfo b_emlrtECI = { 1, 7, 14, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtDCInfo i_emlrtDCI = { 9, 26, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 4 };

static emlrtDCInfo j_emlrtDCI = { 9, 26, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtRTEInfo d_emlrtRTEI = { 10, 1, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtBCInfo emlrtBCI = { -1, -1, 6, 10, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtECInfo c_emlrtECI = { -1, 6, 1, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtBCInfo b_emlrtBCI = { -1, -1, 11, 29, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo c_emlrtBCI = { -1, -1, 11, 33, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtRTEInfo e_emlrtRTEI = { 15, 1, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRTEInfo f_emlrtRTEI = { 16, 5, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtBCInfo d_emlrtBCI = { -1, -1, 7, 9, "meh", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtECInfo d_emlrtECI = { -1, 7, 1, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtBCInfo e_emlrtBCI = { -1, -1, 17, 35, "meh", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo f_emlrtBCI = { -1, -1, 17, 39, "meh", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo g_emlrtBCI = { -1, -1, 17, 13, "meh", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo h_emlrtBCI = { -1, -1, 17, 17, "meh", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtRTEInfo g_emlrtRTEI = { 20, 5, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtRTEInfo h_emlrtRTEI = { 21, 9, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtBCInfo i_emlrtBCI = { -1, -1, 22, 32, "meh", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo j_emlrtBCI = { -1, -1, 22, 36, "meh", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo k_emlrtBCI = { -1, -1, 25, 29, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo k_emlrtDCI = { 25, 33, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo l_emlrtBCI = { -1, -1, 25, 33, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo m_emlrtBCI = { -1, -1, 11, 15, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo n_emlrtBCI = { -1, -1, 26, 35, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo l_emlrtDCI = { 26, 37, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo o_emlrtBCI = { -1, -1, 26, 37, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo p_emlrtBCI = { -1, -1, 29, 26, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo m_emlrtDCI = { 29, 30, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo q_emlrtBCI = { -1, -1, 29, 30, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo r_emlrtBCI = { -1, -1, 32, 26, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo n_emlrtDCI = { 32, 30, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo s_emlrtBCI = { -1, -1, 32, 30, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo t_emlrtBCI = { -1, -1, 36, 22, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo o_emlrtDCI = { 36, 26, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo u_emlrtBCI = { -1, -1, 36, 26, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtRTEInfo i_emlrtRTEI = { 40, 9, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m" };

static emlrtBCInfo v_emlrtBCI = { -1, -1, 41, 33, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo p_emlrtDCI = { 41, 37, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo w_emlrtBCI = { -1, -1, 41, 37, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo x_emlrtBCI = { -1, -1, 44, 29, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo q_emlrtDCI = { 44, 33, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo y_emlrtBCI = { -1, -1, 44, 33, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo ab_emlrtBCI = { -1, -1, 45, 35, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo r_emlrtDCI = { 45, 37, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo bb_emlrtBCI = { -1, -1, 45, 37, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo cb_emlrtBCI = { -1, -1, 48, 26, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo s_emlrtDCI = { 48, 30, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo db_emlrtBCI = { -1, -1, 48, 30, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo eb_emlrtBCI = { -1, -1, 51, 26, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo t_emlrtDCI = { 51, 30, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo fb_emlrtBCI = { -1, -1, 51, 30, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo gb_emlrtBCI = { -1, -1, 55, 22, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo u_emlrtDCI = { 55, 26, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo hb_emlrtBCI = { -1, -1, 55, 26, "good", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo ib_emlrtBCI = { -1, -1, 56, 25, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo jb_emlrtBCI = { -1, -1, 56, 27, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo v_emlrtDCI = { 56, 27, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo kb_emlrtBCI = { -1, -1, 52, 29, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo lb_emlrtBCI = { -1, -1, 52, 31, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo w_emlrtDCI = { 52, 31, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo mb_emlrtBCI = { -1, -1, 49, 29, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo nb_emlrtBCI = { -1, -1, 49, 31, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo x_emlrtDCI = { 49, 31, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo ob_emlrtBCI = { -1, -1, 37, 25, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo pb_emlrtBCI = { -1, -1, 37, 27, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo y_emlrtDCI = { 37, 27, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo qb_emlrtBCI = { -1, -1, 33, 29, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo rb_emlrtBCI = { -1, -1, 33, 31, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo ab_emlrtDCI = { 33, 31, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo sb_emlrtBCI = { -1, -1, 30, 29, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtBCInfo tb_emlrtBCI = { -1, -1, 30, 31, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

static emlrtDCInfo bb_emlrtDCI = { 30, 31, "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 1 };

static emlrtBCInfo ub_emlrtBCI = { -1, -1, 11, 13, "goodfit", "pseudoAlgorithm",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\pseudoAlgorithm.m", 0 };

/* Function Definitions */
void pseudoAlgorithm(const emlrtStack *sp, real_T nsamples, real_T goodsize,
                     real_T mehsize, const real_T kdBruhns[24], const real_T
                     tnpbsa[2], const real_T mfiAdjMean[192], const real_T best
                     [7], const real_T meanPerCond[48], const real_T stdPerCond
                     [48], const real_T biCoefMat[676], emxArray_real_T *good,
                     emxArray_real_T *goodfit, emxArray_real_T *meh)
{
  int32_T i0;
  real_T r;
  real_T y;
  int32_T loop_ub;
  emxArray_real_T *r0;
  emxArray_real_T *r1;
  emxArray_real_T *b_r;
  int32_T k;
  emxArray_int32_T *r2;
  emxArray_real_T *r3;
  int32_T unnamed_idx_0;
  int32_T i1;
  int32_T iv0[2];
  int32_T iv1[2];
  int32_T j;
  real_T b_good[11];
  int32_T b_k;
  real_T temp[11];
  real_T c_r[9];
  boolean_T x[9];
  boolean_T guard1 = false;
  int32_T l;
  real_T tempfit;
  real_T goodtemp[11];
  emlrtStack st;
  (void)best;
  st.prev = sp;
  st.tls = sp->tls;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);
  i0 = good->size[0] * good->size[1] * good->size[2];
  if (!(goodsize > 0.0)) {
    emlrtNonNegativeCheckR2012b(goodsize, &emlrtDCI, sp);
  }

  if (goodsize != (int32_T)muDoubleScalarFloor(goodsize)) {
    emlrtIntegerCheckR2012b(goodsize, &b_emlrtDCI, sp);
  }

  good->size[0] = (int32_T)goodsize;
  good->size[1] = 11;
  r = nsamples * (goodsize + mehsize) + 1.0;
  if (!(r > 0.0)) {
    emlrtNonNegativeCheckR2012b(r, &c_emlrtDCI, sp);
  }

  if (r != (int32_T)muDoubleScalarFloor(r)) {
    emlrtIntegerCheckR2012b(r, &d_emlrtDCI, sp);
  }

  good->size[2] = (int32_T)r;
  emxEnsureCapacity(sp, (emxArray__common *)good, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  if (!(goodsize > 0.0)) {
    emlrtNonNegativeCheckR2012b(goodsize, &emlrtDCI, sp);
  }

  r = goodsize;
  if (r != (int32_T)muDoubleScalarFloor(r)) {
    emlrtIntegerCheckR2012b(r, &b_emlrtDCI, sp);
  }

  y = nsamples * (goodsize + mehsize) + 1.0;
  if (!(y > 0.0)) {
    emlrtNonNegativeCheckR2012b(y, &c_emlrtDCI, sp);
  }

  if (y != (int32_T)muDoubleScalarFloor(y)) {
    emlrtIntegerCheckR2012b(y, &d_emlrtDCI, sp);
  }

  loop_ub = (int32_T)r * 11 * (int32_T)y;
  for (i0 = 0; i0 < loop_ub; i0++) {
    good->data[i0] = 0.0;
  }

  i0 = meh->size[0] * meh->size[1] * meh->size[2];
  if (!(mehsize > 0.0)) {
    emlrtNonNegativeCheckR2012b(mehsize, &e_emlrtDCI, sp);
  }

  if (mehsize != (int32_T)muDoubleScalarFloor(mehsize)) {
    emlrtIntegerCheckR2012b(mehsize, &f_emlrtDCI, sp);
  }

  meh->size[0] = (int32_T)mehsize;
  meh->size[1] = 11;
  if (!(nsamples + 1.0 > 0.0)) {
    emlrtNonNegativeCheckR2012b(nsamples + 1.0, &g_emlrtDCI, sp);
  }

  if (nsamples + 1.0 != (int32_T)muDoubleScalarFloor(nsamples + 1.0)) {
    emlrtIntegerCheckR2012b(nsamples + 1.0, &h_emlrtDCI, sp);
  }

  meh->size[2] = (int32_T)(nsamples + 1.0);
  emxEnsureCapacity(sp, (emxArray__common *)meh, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  if (!(mehsize > 0.0)) {
    emlrtNonNegativeCheckR2012b(mehsize, &e_emlrtDCI, sp);
  }

  r = mehsize;
  if (r != (int32_T)muDoubleScalarFloor(r)) {
    emlrtIntegerCheckR2012b(r, &f_emlrtDCI, sp);
  }

  if (!(nsamples + 1.0 > 0.0)) {
    emlrtNonNegativeCheckR2012b(nsamples + 1.0, &g_emlrtDCI, sp);
  }

  y = nsamples + 1.0;
  if (y != (int32_T)muDoubleScalarFloor(y)) {
    emlrtIntegerCheckR2012b(y, &h_emlrtDCI, sp);
  }

  loop_ub = (int32_T)r * 11 * (int32_T)y;
  for (i0 = 0; i0 < loop_ub; i0++) {
    meh->data[i0] = 0.0;
  }

  emxInit_real_T(sp, &r0, 1, &emlrtRTEI, true);
  emxInit_real_T(sp, &r1, 1, &emlrtRTEI, true);
  emxInit_real_T1(sp, &b_r, 2, &emlrtRTEI, true);
  st.site = &emlrtRSI;
  randi(&st, goodsize, r0);
  st.site = &emlrtRSI;
  b_randi(&st, goodsize, r1);
  st.site = &emlrtRSI;
  i0 = b_r->size[0] * b_r->size[1];
  b_r->size[0] = (int32_T)goodsize;
  b_r->size[1] = 9;
  emxEnsureCapacity(&st, (emxArray__common *)b_r, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  emlrtRandu(&b_r->data[0], b_r->size[0] * 9);
  i0 = b_r->size[0] * b_r->size[1];
  b_r->size[1] = 9;
  emxEnsureCapacity(sp, (emxArray__common *)b_r, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  k = b_r->size[0];
  loop_ub = b_r->size[1];
  loop_ub *= k;
  for (i0 = 0; i0 < loop_ub; i0++) {
    b_r->data[i0] *= 25.0;
  }

  emxInit_int32_T(sp, &r2, 1, &emlrtRTEI, true);
  k = r0->size[0];
  i0 = b_r->size[0];
  if (i0 != k) {
    emlrtDimSizeEqCheckR2012b(i0, k, &emlrtECI, sp);
  }

  k = r1->size[0];
  i0 = b_r->size[0];
  if (i0 != k) {
    emlrtDimSizeEqCheckR2012b(i0, k, &emlrtECI, sp);
  }

  loop_ub = (int32_T)goodsize;
  i0 = r2->size[0];
  r2->size[0] = (int32_T)goodsize;
  emxEnsureCapacity(sp, (emxArray__common *)r2, i0, (int32_T)sizeof(int32_T),
                    &emlrtRTEI);
  for (i0 = 0; i0 < loop_ub; i0++) {
    r2->data[i0] = i0;
  }

  emxInit_real_T1(sp, &r3, 2, &emlrtRTEI, true);
  i0 = (int32_T)(nsamples * (goodsize + mehsize) + 1.0);
  if (!(1 <= i0)) {
    emlrtDynamicBoundsCheckR2012b(1, 1, i0, &emlrtBCI, sp);
  }

  k = r0->size[0];
  unnamed_idx_0 = r1->size[0];
  i0 = r3->size[0] * r3->size[1];
  r3->size[0] = b_r->size[0];
  r3->size[1] = 11;
  emxEnsureCapacity(sp, (emxArray__common *)r3, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  for (i0 = 0; i0 < 9; i0++) {
    loop_ub = b_r->size[0];
    for (i1 = 0; i1 < loop_ub; i1++) {
      r3->data[i1 + r3->size[0] * i0] = b_r->data[i1 + b_r->size[0] * i0] - 20.0;
    }
  }

  for (i0 = 0; i0 < k; i0++) {
    r3->data[i0 + r3->size[0] * 9] = r0->data[i0];
  }

  for (i0 = 0; i0 < unnamed_idx_0; i0++) {
    r3->data[i0 + r3->size[0] * 10] = r1->data[i0];
  }

  iv0[0] = r2->size[0];
  iv0[1] = 11;
  emlrtSubAssignSizeCheckR2012b(iv0, 2, *(int32_T (*)[2])r3->size, 2,
    &c_emlrtECI, sp);
  for (i0 = 0; i0 < 11; i0++) {
    loop_ub = r3->size[0];
    for (i1 = 0; i1 < loop_ub; i1++) {
      good->data[r2->data[i1] + good->size[0] * i0] = r3->data[i1 + r3->size[0] *
        i0];
    }
  }

  st.site = &b_emlrtRSI;
  randi(&st, mehsize, r0);
  st.site = &b_emlrtRSI;
  b_randi(&st, mehsize, r1);
  st.site = &b_emlrtRSI;
  i0 = b_r->size[0] * b_r->size[1];
  b_r->size[0] = (int32_T)mehsize;
  b_r->size[1] = 9;
  emxEnsureCapacity(&st, (emxArray__common *)b_r, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  emlrtRandu(&b_r->data[0], b_r->size[0] * 9);
  i0 = b_r->size[0] * b_r->size[1];
  b_r->size[1] = 9;
  emxEnsureCapacity(sp, (emxArray__common *)b_r, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  k = b_r->size[0];
  loop_ub = b_r->size[1];
  loop_ub *= k;
  for (i0 = 0; i0 < loop_ub; i0++) {
    b_r->data[i0] *= 25.0;
  }

  k = r0->size[0];
  i0 = b_r->size[0];
  if (i0 != k) {
    emlrtDimSizeEqCheckR2012b(i0, k, &b_emlrtECI, sp);
  }

  k = r1->size[0];
  i0 = b_r->size[0];
  if (i0 != k) {
    emlrtDimSizeEqCheckR2012b(i0, k, &b_emlrtECI, sp);
  }

  loop_ub = (int32_T)mehsize;
  i0 = r2->size[0];
  r2->size[0] = (int32_T)mehsize;
  emxEnsureCapacity(sp, (emxArray__common *)r2, i0, (int32_T)sizeof(int32_T),
                    &emlrtRTEI);
  for (i0 = 0; i0 < loop_ub; i0++) {
    r2->data[i0] = i0;
  }

  i0 = (int32_T)(nsamples + 1.0);
  if (!(1 <= i0)) {
    emlrtDynamicBoundsCheckR2012b(1, 1, i0, &d_emlrtBCI, sp);
  }

  k = r0->size[0];
  unnamed_idx_0 = r1->size[0];
  i0 = r3->size[0] * r3->size[1];
  r3->size[0] = b_r->size[0];
  r3->size[1] = 11;
  emxEnsureCapacity(sp, (emxArray__common *)r3, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  for (i0 = 0; i0 < 9; i0++) {
    loop_ub = b_r->size[0];
    for (i1 = 0; i1 < loop_ub; i1++) {
      r3->data[i1 + r3->size[0] * i0] = b_r->data[i1 + b_r->size[0] * i0] - 20.0;
    }
  }

  emxFree_real_T(&b_r);
  for (i0 = 0; i0 < k; i0++) {
    r3->data[i0 + r3->size[0] * 9] = r0->data[i0];
  }

  emxFree_real_T(&r0);
  for (i0 = 0; i0 < unnamed_idx_0; i0++) {
    r3->data[i0 + r3->size[0] * 10] = r1->data[i0];
  }

  emxFree_real_T(&r1);
  iv1[0] = r2->size[0];
  iv1[1] = 11;
  emlrtSubAssignSizeCheckR2012b(iv1, 2, *(int32_T (*)[2])r3->size, 2,
    &d_emlrtECI, sp);
  for (i0 = 0; i0 < 11; i0++) {
    loop_ub = r3->size[0];
    for (i1 = 0; i1 < loop_ub; i1++) {
      meh->data[r2->data[i1] + meh->size[0] * i0] = r3->data[i1 + r3->size[0] *
        i0];
    }
  }

  emxFree_real_T(&r3);
  emxFree_int32_T(&r2);
  i0 = goodfit->size[0] * goodfit->size[1];
  goodfit->size[0] = (int32_T)goodsize;
  r = nsamples * (goodsize + mehsize) + 1.0;
  if (!(r > 0.0)) {
    emlrtNonNegativeCheckR2012b(r, &i_emlrtDCI, sp);
  }

  if (r != (int32_T)muDoubleScalarFloor(r)) {
    emlrtIntegerCheckR2012b(r, &j_emlrtDCI, sp);
  }

  goodfit->size[1] = (int32_T)r;
  emxEnsureCapacity(sp, (emxArray__common *)goodfit, i0, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  r = nsamples * (goodsize + mehsize) + 1.0;
  if (!(r > 0.0)) {
    emlrtNonNegativeCheckR2012b(r, &i_emlrtDCI, sp);
  }

  if (r != (int32_T)muDoubleScalarFloor(r)) {
    emlrtIntegerCheckR2012b(r, &j_emlrtDCI, sp);
  }

  loop_ub = (int32_T)goodsize * (int32_T)r;
  for (i0 = 0; i0 < loop_ub; i0++) {
    goodfit->data[i0] = 0.0;
  }

  emlrtForLoopVectorCheckR2012b(1.0, 1.0, goodsize, mxDOUBLE_CLASS, (int32_T)
    goodsize, &d_emlrtRTEI, sp);
  j = 1;
  while (j - 1 <= (int32_T)goodsize - 1) {
    i0 = goodfit->size[1];
    if (!(1 <= i0)) {
      emlrtDynamicBoundsCheckR2012b(1, 1, i0, &m_emlrtBCI, sp);
    }

    i0 = good->size[2];
    if (!(1 <= i0)) {
      emlrtDynamicBoundsCheckR2012b(1, 1, i0, &c_emlrtBCI, sp);
    }

    i0 = good->size[0];
    if (!((j >= 1) && (j <= i0))) {
      emlrtDynamicBoundsCheckR2012b(j, 1, i0, &b_emlrtBCI, sp);
    }

    for (i0 = 0; i0 < 11; i0++) {
      b_good[i0] = good->data[(j + good->size[0] * i0) - 1];
    }

    i0 = goodfit->size[0];
    if (!((j >= 1) && (j <= i0))) {
      emlrtDynamicBoundsCheckR2012b(j, 1, i0, &ub_emlrtBCI, sp);
    }

    st.site = &c_emlrtRSI;
    goodfit->data[j - 1] = PDF(&st, b_good, kdBruhns, mfiAdjMean, biCoefMat,
      tnpbsa, meanPerCond, stdPerCond);
    j++;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  emlrtForLoopVectorCheckR2012b(1.0, 1.0, nsamples, mxDOUBLE_CLASS, (int32_T)
    nsamples, &e_emlrtRTEI, sp);
  j = 0;
  while (j <= (int32_T)nsamples - 1) {
    emlrtForLoopVectorCheckR2012b(1.0, 1.0, mehsize, mxDOUBLE_CLASS, (int32_T)
      mehsize, &f_emlrtRTEI, sp);
    b_k = 0;
    while (b_k <= (int32_T)mehsize - 1) {
      st.site = &d_emlrtRSI;
      i0 = meh->size[0];
      i1 = b_k + 1;
      if (!((i1 >= 1) && (i1 <= i0))) {
        emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &e_emlrtBCI, &st);
      }

      i0 = meh->size[2];
      i1 = j + 1;
      if (!((i1 >= 1) && (i1 <= i0))) {
        emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &f_emlrtBCI, &st);
      }

      memset(&temp[0], 0, 11U * sizeof(real_T));
      emlrtRandn(c_r, 9);
      for (i0 = 0; i0 < 9; i0++) {
        c_r[i0] *= 0.1;
      }

      for (i0 = 0; i0 < 9; i0++) {
        temp[i0] = meh->data[(b_k + meh->size[0] * i0) + meh->size[0] *
          meh->size[1] * j] + c_r[i0];
      }

      for (i0 = 0; i0 < 9; i0++) {
        x[i0] = (temp[i0] <= -20.0);
      }

      y = x[0];
      for (k = 0; k < 8; k++) {
        y += (real_T)x[k + 1];
      }

      guard1 = false;
      if (y != 0.0) {
        guard1 = true;
      } else {
        for (i0 = 0; i0 < 9; i0++) {
          x[i0] = (temp[i0] >= 5.0);
        }

        y = x[0];
        for (k = 0; k < 8; k++) {
          y += (real_T)x[k + 1];
        }

        if (y != 0.0) {
          guard1 = true;
        } else {
          while ((temp[9] < 1.0) || (4.0 < temp[9])) {
            emlrtRandu(&r, 1);
            temp[9] = (meh->data[(b_k + meh->size[0] * 9) + meh->size[0] *
                       meh->size[1] * j] + (1.0 + muDoubleScalarFloor(r * 3.0)))
              - 2.0;
            if (*emlrtBreakCheckR2012bFlagVar != 0) {
              emlrtBreakCheckR2012b(&st);
            }
          }

          while ((temp[10] < 1.0) || (26.0 < temp[10])) {
            emlrtRandu(&r, 1);
            temp[10] = (meh->data[(b_k + meh->size[0] * 10) + meh->size[0] *
                        meh->size[1] * j] + (1.0 + muDoubleScalarFloor(r * 3.0)))
              - 2.0;
            if (*emlrtBreakCheckR2012bFlagVar != 0) {
              emlrtBreakCheckR2012b(&st);
            }
          }
        }
      }

      if (guard1) {
        emlrtRandu(c_r, 9);
        emlrtRandu(&r, 1);
        emlrtRandu(&y, 1);
        for (i0 = 0; i0 < 9; i0++) {
          temp[i0] = 25.0 * c_r[i0] - 20.0;
        }

        temp[9] = 1.0 + muDoubleScalarFloor(r * 4.0);
        temp[10] = 1.0 + muDoubleScalarFloor(y * 26.0);
      }

      k = meh->size[0];
      loop_ub = meh->size[2];
      i0 = (int32_T)((1.0 + (real_T)j) + 1.0);
      if (!((i0 >= 1) && (i0 <= loop_ub))) {
        emlrtDynamicBoundsCheckR2012b(i0, 1, loop_ub, &h_emlrtBCI, sp);
      }

      if (!((b_k + 1 >= 1) && (b_k + 1 <= k))) {
        emlrtDynamicBoundsCheckR2012b(b_k + 1, 1, k, &g_emlrtBCI, sp);
      }

      for (i0 = 0; i0 < 11; i0++) {
        meh->data[(b_k + meh->size[0] * i0) + meh->size[0] * meh->size[1] *
          ((int32_T)((1.0 + (real_T)j) + 1.0) - 1)] = temp[i0];
      }

      b_k++;
      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(sp);
      }
    }

    emlrtForLoopVectorCheckR2012b(1.0, 1.0, goodsize, mxDOUBLE_CLASS, (int32_T)
      goodsize, &g_emlrtRTEI, sp);
    b_k = 1;
    while (b_k - 1 <= (int32_T)goodsize - 1) {
      emlrtForLoopVectorCheckR2012b(1.0, 1.0, mehsize, mxDOUBLE_CLASS, (int32_T)
        mehsize, &h_emlrtRTEI, sp);
      l = 0;
      while (l <= (int32_T)mehsize - 1) {
        i0 = meh->size[2];
        if (!((j + 1 >= 1) && (j + 1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(j + 1, 1, i0, &j_emlrtBCI, sp);
        }

        k = j + 1;
        i0 = meh->size[0];
        if (!((l + 1 >= 1) && (l + 1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(l + 1, 1, i0, &i_emlrtBCI, sp);
        }

        loop_ub = l + 1;
        for (i0 = 0; i0 < 11; i0++) {
          b_good[i0] = meh->data[((loop_ub + meh->size[0] * i0) + meh->size[0] *
            meh->size[1] * (k - 1)) - 1];
        }

        st.site = &e_emlrtRSI;
        PROPRND(&st, b_good, temp);
        st.site = &f_emlrtRSI;
        tempfit = PDF(&st, temp, kdBruhns, mfiAdjMean, biCoefMat, tnpbsa,
                      meanPerCond, stdPerCond);
        r = ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize) + (1.0 + (real_T)l);
        if (r != (int32_T)muDoubleScalarFloor(r)) {
          emlrtIntegerCheckR2012b(r, &k_emlrtDCI, sp);
        }

        i0 = good->size[2];
        i1 = (int32_T)r;
        if (!((i1 >= 1) && (i1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &l_emlrtBCI, sp);
        }

        i0 = good->size[0];
        if (!((b_k >= 1) && (b_k <= i0))) {
          emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &k_emlrtBCI, sp);
        }

        for (i0 = 0; i0 < 11; i0++) {
          goodtemp[i0] = good->data[((b_k + good->size[0] * i0) + good->size[0] *
            good->size[1] * (i1 - 1)) - 1];
        }

        i0 = goodfit->size[0];
        i1 = (b_k - 1) + 1;
        if (!((i1 >= 1) && (i1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &n_emlrtBCI, sp);
        }

        r = ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize) + (1.0 + (real_T)l);
        if (r != (int32_T)muDoubleScalarFloor(r)) {
          emlrtIntegerCheckR2012b(r, &l_emlrtDCI, sp);
        }

        i0 = goodfit->size[1];
        i1 = (int32_T)r;
        if (!((i1 >= 1) && (i1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &o_emlrtBCI, sp);
        }

        if (tempfit - goodfit->data[(b_k + goodfit->size[0] * ((int32_T)(((1.0 +
                 (real_T)j) - 1.0) * (goodsize + mehsize) + (1.0 + (real_T)l)) -
              1)) - 1] < 0.0) {
          st.site = &g_emlrtRSI;
          emlrtRandu(&r, 1);
          if (r < muDoubleScalarExp(tempfit - goodfit->data[(b_k + goodfit->
                size[0] * ((int32_T)(((1.0 + (real_T)j) - 1.0) * (goodsize +
                   mehsize) + (1.0 + (real_T)l)) - 1)) - 1])) {
            k = good->size[0];
            loop_ub = good->size[2];
            r = (1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) + (1.0
              + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &m_emlrtDCI, sp);
            }

            i0 = (int32_T)r;
            if (!((i0 >= 1) && (i0 <= loop_ub))) {
              emlrtDynamicBoundsCheckR2012b(i0, 1, loop_ub, &q_emlrtBCI, sp);
            }

            if (!((b_k >= 1) && (b_k <= k))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, k, &p_emlrtBCI, sp);
            }

            for (i1 = 0; i1 < 11; i1++) {
              good->data[((b_k + good->size[0] * i1) + good->size[0] *
                          good->size[1] * (i0 - 1)) - 1] = temp[i1];
            }

            i0 = goodfit->size[0];
            if (!((b_k >= 1) && (b_k <= i0))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &sb_emlrtBCI, sp);
            }

            i0 = goodfit->size[1];
            r = (1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) + (1.0
              + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &bb_emlrtDCI, sp);
            }

            i1 = (int32_T)r;
            if (!((i1 >= 1) && (i1 <= i0))) {
              emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &tb_emlrtBCI, sp);
            }

            goodfit->data[(b_k + goodfit->size[0] * (i1 - 1)) - 1] = tempfit;
          } else {
            k = good->size[0];
            loop_ub = good->size[2];
            r = (1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) + (1.0
              + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &n_emlrtDCI, sp);
            }

            i0 = (int32_T)r;
            if (!((i0 >= 1) && (i0 <= loop_ub))) {
              emlrtDynamicBoundsCheckR2012b(i0, 1, loop_ub, &s_emlrtBCI, sp);
            }

            if (!((b_k >= 1) && (b_k <= k))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, k, &r_emlrtBCI, sp);
            }

            for (i1 = 0; i1 < 11; i1++) {
              good->data[((b_k + good->size[0] * i1) + good->size[0] *
                          good->size[1] * (i0 - 1)) - 1] = goodtemp[i1];
            }

            i0 = goodfit->size[0];
            if (!((b_k >= 1) && (b_k <= i0))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &qb_emlrtBCI, sp);
            }

            i0 = goodfit->size[1];
            r = (1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) + (1.0
              + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &ab_emlrtDCI, sp);
            }

            i1 = (int32_T)r;
            if (!((i1 >= 1) && (i1 <= i0))) {
              emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &rb_emlrtBCI, sp);
            }

            goodfit->data[(b_k + goodfit->size[0] * (i1 - 1)) - 1] =
              goodfit->data[(b_k + goodfit->size[0] * ((int32_T)(((1.0 + (real_T)
              j) - 1.0) * (goodsize + mehsize) + (1.0 + (real_T)l)) - 1)) - 1];
          }
        } else {
          k = good->size[0];
          loop_ub = good->size[2];
          r = (1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) + (1.0 +
            (real_T)l);
          if (r != (int32_T)muDoubleScalarFloor(r)) {
            emlrtIntegerCheckR2012b(r, &o_emlrtDCI, sp);
          }

          i0 = (int32_T)r;
          if (!((i0 >= 1) && (i0 <= loop_ub))) {
            emlrtDynamicBoundsCheckR2012b(i0, 1, loop_ub, &u_emlrtBCI, sp);
          }

          if (!((b_k >= 1) && (b_k <= k))) {
            emlrtDynamicBoundsCheckR2012b(b_k, 1, k, &t_emlrtBCI, sp);
          }

          for (i1 = 0; i1 < 11; i1++) {
            good->data[((b_k + good->size[0] * i1) + good->size[0] * good->size
                        [1] * (i0 - 1)) - 1] = temp[i1];
          }

          i0 = goodfit->size[0];
          if (!((b_k >= 1) && (b_k <= i0))) {
            emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &ob_emlrtBCI, sp);
          }

          i0 = goodfit->size[1];
          r = (1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) + (1.0 +
            (real_T)l);
          if (r != (int32_T)muDoubleScalarFloor(r)) {
            emlrtIntegerCheckR2012b(r, &y_emlrtDCI, sp);
          }

          i1 = (int32_T)r;
          if (!((i1 >= 1) && (i1 <= i0))) {
            emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &pb_emlrtBCI, sp);
          }

          goodfit->data[(b_k + goodfit->size[0] * (i1 - 1)) - 1] = tempfit;
        }

        l++;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }

      emlrtForLoopVectorCheckR2012b(1.0, 1.0, goodsize, mxDOUBLE_CLASS, (int32_T)
        goodsize, &i_emlrtRTEI, sp);
      l = 0;
      while (l <= (int32_T)goodsize - 1) {
        r = (((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize) + mehsize) + (1.0
          + (real_T)l);
        if (r != (int32_T)muDoubleScalarFloor(r)) {
          emlrtIntegerCheckR2012b(r, &p_emlrtDCI, sp);
        }

        i0 = good->size[2];
        i1 = (int32_T)r;
        if (!((i1 >= 1) && (i1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &w_emlrtBCI, sp);
        }

        i0 = good->size[0];
        if (!((l + 1 >= 1) && (l + 1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(l + 1, 1, i0, &v_emlrtBCI, sp);
        }

        loop_ub = l + 1;
        for (i0 = 0; i0 < 11; i0++) {
          b_good[i0] = good->data[((loop_ub + good->size[0] * i0) + good->size[0]
            * good->size[1] * (i1 - 1)) - 1];
        }

        st.site = &h_emlrtRSI;
        PROPRND(&st, b_good, temp);
        st.site = &i_emlrtRSI;
        tempfit = PDF(&st, temp, kdBruhns, mfiAdjMean, biCoefMat, tnpbsa,
                      meanPerCond, stdPerCond);
        r = (((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize) + mehsize) + (1.0
          + (real_T)l);
        if (r != (int32_T)muDoubleScalarFloor(r)) {
          emlrtIntegerCheckR2012b(r, &q_emlrtDCI, sp);
        }

        i0 = good->size[2];
        i1 = (int32_T)r;
        if (!((i1 >= 1) && (i1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &y_emlrtBCI, sp);
        }

        i0 = good->size[0];
        if (!((b_k >= 1) && (b_k <= i0))) {
          emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &x_emlrtBCI, sp);
        }

        for (i0 = 0; i0 < 11; i0++) {
          goodtemp[i0] = good->data[((b_k + good->size[0] * i0) + good->size[0] *
            good->size[1] * (i1 - 1)) - 1];
        }

        i0 = goodfit->size[0];
        i1 = (b_k - 1) + 1;
        if (!((i1 >= 1) && (i1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &ab_emlrtBCI, sp);
        }

        r = (((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize) + mehsize) + (1.0
          + (real_T)l);
        if (r != (int32_T)muDoubleScalarFloor(r)) {
          emlrtIntegerCheckR2012b(r, &r_emlrtDCI, sp);
        }

        i0 = goodfit->size[1];
        i1 = (int32_T)r;
        if (!((i1 >= 1) && (i1 <= i0))) {
          emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &bb_emlrtBCI, sp);
        }

        if (tempfit - goodfit->data[(b_k + goodfit->size[0] * ((int32_T)((((1.0
                  + (real_T)j) - 1.0) * (goodsize + mehsize) + mehsize) + (1.0 +
                (real_T)l)) - 1)) - 1] < 0.0) {
          st.site = &j_emlrtRSI;
          emlrtRandu(&r, 1);
          if (r < muDoubleScalarExp(tempfit - goodfit->data[(b_k + goodfit->
                size[0] * ((int32_T)((((1.0 + (real_T)j) - 1.0) * (goodsize +
                    mehsize) + mehsize) + (1.0 + (real_T)l)) - 1)) - 1])) {
            k = good->size[0];
            loop_ub = good->size[2];
            r = ((1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) +
                 mehsize) + (1.0 + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &s_emlrtDCI, sp);
            }

            i0 = (int32_T)r;
            if (!((i0 >= 1) && (i0 <= loop_ub))) {
              emlrtDynamicBoundsCheckR2012b(i0, 1, loop_ub, &db_emlrtBCI, sp);
            }

            if (!((b_k >= 1) && (b_k <= k))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, k, &cb_emlrtBCI, sp);
            }

            for (i1 = 0; i1 < 11; i1++) {
              good->data[((b_k + good->size[0] * i1) + good->size[0] *
                          good->size[1] * (i0 - 1)) - 1] = temp[i1];
            }

            i0 = goodfit->size[0];
            if (!((b_k >= 1) && (b_k <= i0))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &mb_emlrtBCI, sp);
            }

            i0 = goodfit->size[1];
            r = ((1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) +
                 mehsize) + (1.0 + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &x_emlrtDCI, sp);
            }

            i1 = (int32_T)r;
            if (!((i1 >= 1) && (i1 <= i0))) {
              emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &nb_emlrtBCI, sp);
            }

            goodfit->data[(b_k + goodfit->size[0] * (i1 - 1)) - 1] = tempfit;
          } else {
            k = good->size[0];
            loop_ub = good->size[2];
            r = ((1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) +
                 mehsize) + (1.0 + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &t_emlrtDCI, sp);
            }

            i0 = (int32_T)r;
            if (!((i0 >= 1) && (i0 <= loop_ub))) {
              emlrtDynamicBoundsCheckR2012b(i0, 1, loop_ub, &fb_emlrtBCI, sp);
            }

            if (!((b_k >= 1) && (b_k <= k))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, k, &eb_emlrtBCI, sp);
            }

            for (i1 = 0; i1 < 11; i1++) {
              good->data[((b_k + good->size[0] * i1) + good->size[0] *
                          good->size[1] * (i0 - 1)) - 1] = goodtemp[i1];
            }

            i0 = goodfit->size[0];
            if (!((b_k >= 1) && (b_k <= i0))) {
              emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &kb_emlrtBCI, sp);
            }

            i0 = goodfit->size[1];
            r = ((1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) +
                 mehsize) + (1.0 + (real_T)l);
            if (r != (int32_T)muDoubleScalarFloor(r)) {
              emlrtIntegerCheckR2012b(r, &w_emlrtDCI, sp);
            }

            i1 = (int32_T)r;
            if (!((i1 >= 1) && (i1 <= i0))) {
              emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &lb_emlrtBCI, sp);
            }

            goodfit->data[(b_k + goodfit->size[0] * (i1 - 1)) - 1] =
              goodfit->data[(b_k + goodfit->size[0] * ((int32_T)((((1.0 +
              (real_T)j) - 1.0) * (goodsize + mehsize) + mehsize) + (1.0 +
              (real_T)l)) - 1)) - 1];
          }
        } else {
          k = good->size[0];
          loop_ub = good->size[2];
          r = ((1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) +
               mehsize) + (1.0 + (real_T)l);
          if (r != (int32_T)muDoubleScalarFloor(r)) {
            emlrtIntegerCheckR2012b(r, &u_emlrtDCI, sp);
          }

          i0 = (int32_T)r;
          if (!((i0 >= 1) && (i0 <= loop_ub))) {
            emlrtDynamicBoundsCheckR2012b(i0, 1, loop_ub, &hb_emlrtBCI, sp);
          }

          if (!((b_k >= 1) && (b_k <= k))) {
            emlrtDynamicBoundsCheckR2012b(b_k, 1, k, &gb_emlrtBCI, sp);
          }

          for (i1 = 0; i1 < 11; i1++) {
            good->data[((b_k + good->size[0] * i1) + good->size[0] * good->size
                        [1] * (i0 - 1)) - 1] = temp[i1];
          }

          i0 = goodfit->size[0];
          if (!((b_k >= 1) && (b_k <= i0))) {
            emlrtDynamicBoundsCheckR2012b(b_k, 1, i0, &ib_emlrtBCI, sp);
          }

          i0 = goodfit->size[1];
          r = ((1.0 + ((1.0 + (real_T)j) - 1.0) * (goodsize + mehsize)) +
               mehsize) + (1.0 + (real_T)l);
          if (r != (int32_T)muDoubleScalarFloor(r)) {
            emlrtIntegerCheckR2012b(r, &v_emlrtDCI, sp);
          }

          i1 = (int32_T)r;
          if (!((i1 >= 1) && (i1 <= i0))) {
            emlrtDynamicBoundsCheckR2012b(i1, 1, i0, &jb_emlrtBCI, sp);
          }

          goodfit->data[(b_k + goodfit->size[0] * (i1 - 1)) - 1] = tempfit;
        }

        l++;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }

      b_k++;
      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(sp);
      }
    }

    j++;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
}

/* End of code generation (pseudoAlgorithm.c) */
