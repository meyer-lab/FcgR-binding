/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Error.c
 *
 * Code generation for function 'Error'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "Error.h"
#include "power.h"
#include "PDF_emxutil.h"
#include "nansum.h"
#include "rdivide.h"
#include "PDF_data.h"

/* Variable Definitions */
static emlrtRSInfo b_emlrtRSI = { 54, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo c_emlrtRSI = { 55, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo d_emlrtRSI = { 62, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo e_emlrtRSI = { 63, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo f_emlrtRSI = { 82, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo g_emlrtRSI = { 21, "colon",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\colon.m" };

static emlrtRSInfo h_emlrtRSI = { 79, "colon",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\colon.m" };

static emlrtRSInfo i_emlrtRSI = { 283, "colon",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\colon.m" };

static emlrtRSInfo j_emlrtRSI = { 291, "colon",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\colon.m" };

static emlrtRTEInfo emlrtRTEI = { 1, 35, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRTEInfo c_emlrtRTEI = { 404, 15, "colon",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\colon.m" };

static emlrtBCInfo c_emlrtBCI = { 1, 8, 128, 13, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtBCInfo d_emlrtBCI = { 1, 192, 113, 27, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtBCInfo e_emlrtBCI = { 1, 192, 100, 23, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtECInfo emlrtECI = { -1, 63, 39, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtECInfo b_emlrtECI = { -1, 62, 38, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtECInfo c_emlrtECI = { -1, 55, 17, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtBCInfo f_emlrtBCI = { 1, 26, 55, 34, "biCoefMat", "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 0 };

static emlrtDCInfo emlrtDCI = { 55, 34, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 1 };

static emlrtBCInfo g_emlrtBCI = { 1, 26, 55, 27, "biCoefMat", "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 0 };

static emlrtDCInfo b_emlrtDCI = { 55, 27, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 1 };

static emlrtECInfo d_emlrtECI = { -1, 54, 16, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtBCInfo h_emlrtBCI = { 1, 26, 54, 33, "biCoefMat", "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 0 };

static emlrtDCInfo c_emlrtDCI = { 54, 33, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 1 };

static emlrtBCInfo i_emlrtBCI = { 1, 26, 54, 26, "biCoefMat", "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 0 };

static emlrtDCInfo d_emlrtDCI = { 54, 26, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m", 1 };

/* Function Declarations */
static int32_T asr_s32(int32_T u, uint32_T n);

/* Function Definitions */
static int32_T asr_s32(int32_T u, uint32_T n)
{
  int32_T y;
  if (u >= 0) {
    y = (int32_T)((uint32_T)u >> n);
  } else {
    y = -(int32_T)((uint32_T)-(u + 1) >> n) - 1;
  }

  return y;
}

void Error(const emlrtStack *sp, real_T Rtot[7], const real_T kd[24], const
           real_T mfiAdjMean4[96], const real_T mfiAdjMean26[96], const real_T
           v[2], const real_T biCoefMat[676], const real_T tnpbsa[2], real_T *J,
           real_T mfiExp_data[], int32_T mfiExp_size[2], real_T mfiExpPre_data[],
           int32_T mfiExpPre_size[2])
{
  real_T b_Rtot[7];
  int32_T i;
  real_T Req4[24];
  real_T Req26[24];
  int32_T j;
  int32_T k;
  real_T b_Req4[24];
  real_T b_Req26[24];
  int32_T loop_ub;
  int32_T iy;
  real_T s;
  real_T apnd;
  boolean_T n_too_large;
  real_T ndbl;
  real_T cdiff;
  emxArray_real_T *y;
  int32_T nm1d2;
  emxArray_real_T *b_y;
  int32_T b_loop_ub;
  emxArray_real_T *r0;
  real_T CoefVec4_data[26];
  emxArray_real_T *c_y;
  real_T CoefVec26_data[26];
  real_T mfiExpPre4[24];
  real_T mfiExpPre26[24];
  emxArray_real_T *r1;
  int32_T ix;
  real_T b_CoefVec4_data[26];
  int32_T CoefVec4_size[1];
  int32_T CoefVec26_size[1];
  real_T b_mfiExpPre4[24];
  real_T b_mfiExpPre26[24];
  real_T c_mfiExpPre4[48];
  real_T mfiExp4[96];
  real_T mfiExp26[96];
  real_T b_mfiExp4[192];
  real_T c_mfiExp4[96];
  real_T dv0[96];
  real_T varargin_1[192];
  real_T d_y[8];
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  emlrtStack d_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;
  d_st.prev = &c_st;
  d_st.tls = c_st.tls;
  emlrtHeapReferenceStackEnterFcnR2012b(sp);
  for (i = 0; i < 7; i++) {
    b_Rtot[i] = Rtot[i];
  }

  power(b_Rtot, Rtot);

  /* Preallocating space for the Req values (according to Stone et al.) for */
  /* each combination of IgG and FcgR per flavor of TNP-X-BSA. */
  for (i = 0; i < 24; i++) {
    Req4[i] = 0.0;
    Req26[i] = 0.0;
  }

  /*      ReqFunc = @(Reqi, R, kdi, Li, vi) R - Reqi*(1+vi*Li/kdi*(1+kx*Reqi)^(vi-1)); */
  /* Finding Req values by means of bisection algorithm */
  j = 0;
  while (j < 6) {
    k = 0;
    while (k < 4) {
      /*              Req4(j,k) = bisection(@(x) ReqFunc(10^x,Rtot(j),kd(j,k),L(1),v(1),kx),-5,5,1e-10); */
      /*              Req26(j,k) = bisection(@(x) ReqFunc(10^x,Rtot(j),kd(j,k),L(2),v(2),kx),-5,5,1e-10); */
      /* %%This function returns the point at which function fun equals zero */
      /* %%using the bisection algorithm. The closest a and b will converge to */
      /* %%in the algorithm is a distance 1e-12 apart. */
      /* Check that the first point on the interval is less than the second,  */
      /* that fun(a)*fun(b) is negative, and that error is positive. If not,  */
      /* return an imaginary number. */
      /* Commence algorithm */
      Req4[j + 6 * k] = 6.0;

      /* %%This function returns the point at which function fun equals zero */
      /* %%using the bisection algorithm. The closest a and b will converge to */
      /* %%in the algorithm is a distance 1e-12 apart. */
      /* Check that the first point on the interval is less than the second,  */
      /* that fun(a)*fun(b) is negative, and that error is positive. If not,  */
      /* return an imaginary number. */
      /* Commence algorithm */
      Req26[j + 6 * k] = 6.0;
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

  /* Preventing errors in global optimization due to failure of the */
  /* above local solver */
  memcpy(&b_Req4[0], &Req4[0], 24U * sizeof(real_T));
  b_power(b_Req4, Req4);
  memcpy(&b_Req26[0], &Req26[0], 24U * sizeof(real_T));
  b_power(b_Req26, Req26);

  /*    R is a seven-dimensional vector whose first six elements are */
  /*    expression levels of FcgRIA, FcgRIIA-Arg, etc. and whose seventh */
  /*    element is kx (see RegressionAndResiduals.m). kd is a 6 X 4 */
  /*    matrix whose elements represent the Kd values associated with each */
  /*    flavor of immunoglobulin per flavor of receptor. tnpbsa is derived in */
  /*    loadData.m, as is mfiAdjMean; v is the valency of the TNP-X-BSA. */
  /* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */
  /* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */
  /* Create a matrix of coefficients of the form: */
  /* v!/((v-i)!*i!)*10^(kx+i-1)*tnpbsa */
  /* for all i from 1 to v for all v from 1 to 10 */
  if (1.0 > v[0]) {
    loop_ub = 0;
  } else {
    if (v[0] != (int32_T)muDoubleScalarFloor(v[0])) {
      emlrtIntegerCheckR2012b(v[0], &d_emlrtDCI, sp);
    }

    loop_ub = (int32_T)v[0];
    if (!((loop_ub >= 1) && (loop_ub <= 26))) {
      emlrtDynamicBoundsCheckR2012b(loop_ub, 1, 26, &i_emlrtBCI, sp);
    }
  }

  if (v[0] != (int32_T)muDoubleScalarFloor(v[0])) {
    emlrtIntegerCheckR2012b(v[0], &c_emlrtDCI, sp);
  }

  i = (int32_T)v[0];
  if (!((i >= 1) && (i <= 26))) {
    emlrtDynamicBoundsCheckR2012b(i, 1, 26, &h_emlrtBCI, sp);
  }

  st.site = &b_emlrtRSI;
  b_st.site = &g_emlrtRSI;
  c_st.site = &h_emlrtRSI;
  if (muDoubleScalarIsNaN(v[0])) {
    iy = 1;
    s = rtNaN;
    apnd = v[0];
    n_too_large = false;
  } else if (v[0] < 1.0) {
    iy = 0;
    s = 1.0;
    apnd = v[0];
    n_too_large = false;
  } else if (muDoubleScalarIsInf(v[0])) {
    iy = 1;
    s = rtNaN;
    apnd = v[0];
    n_too_large = !(1.0 == v[0]);
  } else {
    s = 1.0;
    ndbl = muDoubleScalarFloor((v[0] - 1.0) + 0.5);
    apnd = 1.0 + ndbl;
    cdiff = (1.0 + ndbl) - v[0];
    if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * v[0]) {
      ndbl++;
      apnd = v[0];
    } else if (cdiff > 0.0) {
      apnd = 1.0 + (ndbl - 1.0);
    } else {
      ndbl++;
    }

    n_too_large = (2.147483647E+9 < ndbl);
    if (ndbl >= 0.0) {
      iy = (int32_T)ndbl;
    } else {
      iy = 0;
    }
  }

  d_st.site = &i_emlrtRSI;
  if (!n_too_large) {
  } else {
    emlrtErrorWithMessageIdR2012b(&d_st, &c_emlrtRTEI, "Coder:MATLAB:pmaxsize",
      0);
  }

  emxInit_real_T1(&d_st, &y, 2, &emlrtRTEI, true);
  i = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = iy;
  emxEnsureCapacity(&c_st, (emxArray__common *)y, i, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  if (iy > 0) {
    y->data[0] = s;
    if (iy > 1) {
      y->data[iy - 1] = apnd;
      i = iy - 1;
      nm1d2 = asr_s32(i, 1U);
      d_st.site = &j_emlrtRSI;
      for (k = 1; k < nm1d2; k++) {
        y->data[k] = s + (real_T)k;
        y->data[(iy - k) - 1] = apnd - (real_T)k;
      }

      if (nm1d2 << 1 == iy - 1) {
        y->data[nm1d2] = (s + apnd) / 2.0;
      } else {
        y->data[nm1d2] = s + (real_T)nm1d2;
        y->data[nm1d2 + 1] = apnd - (real_T)nm1d2;
      }
    }
  }

  emxInit_real_T(&c_st, &b_y, 1, &emlrtRTEI, true);
  i = b_y->size[0];
  b_y->size[0] = y->size[1];
  emxEnsureCapacity(sp, (emxArray__common *)b_y, i, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  b_loop_ub = y->size[1];
  for (i = 0; i < b_loop_ub; i++) {
    b_y->data[i] = y->data[y->size[0] * i] - 1.0;
  }

  emxInit_real_T(sp, &r0, 1, &emlrtRTEI, true);
  st.site = &b_emlrtRSI;
  c_power(&st, Rtot[0], b_y, r0);
  i = r0->size[0];
  if (loop_ub != i) {
    emlrtSizeEqCheck1DR2012b(loop_ub, i, &d_emlrtECI, sp);
  }

  emxFree_real_T(&b_y);
  for (i = 0; i < loop_ub; i++) {
    CoefVec4_data[i] = biCoefMat[i + 26 * ((int32_T)v[0] - 1)] * r0->data[i] *
      tnpbsa[0];
  }

  if (1.0 > v[1]) {
    b_loop_ub = 0;
  } else {
    if (v[1] != (int32_T)muDoubleScalarFloor(v[1])) {
      emlrtIntegerCheckR2012b(v[1], &b_emlrtDCI, sp);
    }

    b_loop_ub = (int32_T)v[1];
    if (!((b_loop_ub >= 1) && (b_loop_ub <= 26))) {
      emlrtDynamicBoundsCheckR2012b(b_loop_ub, 1, 26, &g_emlrtBCI, sp);
    }
  }

  if (v[1] != (int32_T)muDoubleScalarFloor(v[1])) {
    emlrtIntegerCheckR2012b(v[1], &emlrtDCI, sp);
  }

  i = (int32_T)v[1];
  if (!((i >= 1) && (i <= 26))) {
    emlrtDynamicBoundsCheckR2012b(i, 1, 26, &f_emlrtBCI, sp);
  }

  st.site = &c_emlrtRSI;
  b_st.site = &g_emlrtRSI;
  c_st.site = &h_emlrtRSI;
  if (muDoubleScalarIsNaN(v[1])) {
    iy = 1;
    s = rtNaN;
    apnd = v[1];
    n_too_large = false;
  } else if (v[1] < 1.0) {
    iy = 0;
    s = 1.0;
    apnd = v[1];
    n_too_large = false;
  } else if (muDoubleScalarIsInf(v[1])) {
    iy = 1;
    s = rtNaN;
    apnd = v[1];
    n_too_large = !(1.0 == v[1]);
  } else {
    s = 1.0;
    ndbl = muDoubleScalarFloor((v[1] - 1.0) + 0.5);
    apnd = 1.0 + ndbl;
    cdiff = (1.0 + ndbl) - v[1];
    if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * v[1]) {
      ndbl++;
      apnd = v[1];
    } else if (cdiff > 0.0) {
      apnd = 1.0 + (ndbl - 1.0);
    } else {
      ndbl++;
    }

    n_too_large = (2.147483647E+9 < ndbl);
    if (ndbl >= 0.0) {
      iy = (int32_T)ndbl;
    } else {
      iy = 0;
    }
  }

  d_st.site = &i_emlrtRSI;
  if (!n_too_large) {
  } else {
    emlrtErrorWithMessageIdR2012b(&d_st, &c_emlrtRTEI, "Coder:MATLAB:pmaxsize",
      0);
  }

  i = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = iy;
  emxEnsureCapacity(&c_st, (emxArray__common *)y, i, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  if (iy > 0) {
    y->data[0] = s;
    if (iy > 1) {
      y->data[iy - 1] = apnd;
      i = iy - 1;
      nm1d2 = asr_s32(i, 1U);
      d_st.site = &j_emlrtRSI;
      for (k = 1; k < nm1d2; k++) {
        y->data[k] = s + (real_T)k;
        y->data[(iy - k) - 1] = apnd - (real_T)k;
      }

      if (nm1d2 << 1 == iy - 1) {
        y->data[nm1d2] = (s + apnd) / 2.0;
      } else {
        y->data[nm1d2] = s + (real_T)nm1d2;
        y->data[nm1d2 + 1] = apnd - (real_T)nm1d2;
      }
    }
  }

  emxInit_real_T(&c_st, &c_y, 1, &emlrtRTEI, true);
  i = c_y->size[0];
  c_y->size[0] = y->size[1];
  emxEnsureCapacity(sp, (emxArray__common *)c_y, i, (int32_T)sizeof(real_T),
                    &emlrtRTEI);
  nm1d2 = y->size[1];
  for (i = 0; i < nm1d2; i++) {
    c_y->data[i] = y->data[y->size[0] * i] - 1.0;
  }

  st.site = &c_emlrtRSI;
  c_power(&st, Rtot[0], c_y, r0);
  i = r0->size[0];
  if (b_loop_ub != i) {
    emlrtSizeEqCheck1DR2012b(b_loop_ub, i, &c_emlrtECI, sp);
  }

  emxFree_real_T(&c_y);
  for (i = 0; i < b_loop_ub; i++) {
    CoefVec26_data[i] = biCoefMat[i + 26 * ((int32_T)v[1] - 1)] * r0->data[i] *
      tnpbsa[1];
  }

  /* Creating matrix of expected MFIs; takes a few steps to do so */
  for (i = 0; i < 24; i++) {
    mfiExpPre4[i] = 0.0;
    mfiExpPre26[i] = 0.0;
  }

  j = 0;
  emxInit_real_T1(sp, &r1, 2, &emlrtRTEI, true);
  while (j < 6) {
    k = 0;
    while (k < 4) {
      st.site = &d_emlrtRSI;
      b_st.site = &g_emlrtRSI;
      c_st.site = &h_emlrtRSI;
      if (muDoubleScalarIsNaN(v[0])) {
        iy = 1;
        s = rtNaN;
        apnd = v[0];
        n_too_large = false;
      } else if (v[0] < 1.0) {
        iy = 0;
        s = 1.0;
        apnd = v[0];
        n_too_large = false;
      } else if (muDoubleScalarIsInf(v[0])) {
        iy = 1;
        s = rtNaN;
        apnd = v[0];
        n_too_large = !(1.0 == v[0]);
      } else {
        s = 1.0;
        ndbl = muDoubleScalarFloor((v[0] - 1.0) + 0.5);
        apnd = 1.0 + ndbl;
        cdiff = (1.0 + ndbl) - v[0];
        if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * v[0]) {
          ndbl++;
          apnd = v[0];
        } else if (cdiff > 0.0) {
          apnd = 1.0 + (ndbl - 1.0);
        } else {
          ndbl++;
        }

        n_too_large = (2.147483647E+9 < ndbl);
        if (ndbl >= 0.0) {
          iy = (int32_T)ndbl;
        } else {
          iy = 0;
        }
      }

      d_st.site = &i_emlrtRSI;
      if (!n_too_large) {
      } else {
        emlrtErrorWithMessageIdR2012b(&d_st, &c_emlrtRTEI,
          "Coder:MATLAB:pmaxsize", 0);
      }

      i = y->size[0] * y->size[1];
      y->size[0] = 1;
      y->size[1] = iy;
      emxEnsureCapacity(&c_st, (emxArray__common *)y, i, (int32_T)sizeof(real_T),
                        &emlrtRTEI);
      if (iy > 0) {
        y->data[0] = s;
        if (iy > 1) {
          y->data[iy - 1] = apnd;
          i = iy - 1;
          nm1d2 = asr_s32(i, 1U);
          d_st.site = &j_emlrtRSI;
          for (ix = 1; ix < nm1d2; ix++) {
            y->data[ix] = s + (real_T)ix;
            y->data[(iy - ix) - 1] = apnd - (real_T)ix;
          }

          if (nm1d2 << 1 == iy - 1) {
            y->data[nm1d2] = (s + apnd) / 2.0;
          } else {
            y->data[nm1d2] = s + (real_T)nm1d2;
            y->data[nm1d2 + 1] = apnd - (real_T)nm1d2;
          }
        }
      }

      st.site = &d_emlrtRSI;
      d_power(&st, Req4[j + 6 * k], y, r1);
      i = r0->size[0];
      r0->size[0] = r1->size[1];
      emxEnsureCapacity(sp, (emxArray__common *)r0, i, (int32_T)sizeof(real_T),
                        &emlrtRTEI);
      nm1d2 = r1->size[1];
      for (i = 0; i < nm1d2; i++) {
        r0->data[i] = r1->data[r1->size[0] * i];
      }

      i = r0->size[0];
      if (loop_ub != i) {
        emlrtSizeEqCheck1DR2012b(loop_ub, i, &b_emlrtECI, sp);
      }

      CoefVec4_size[0] = loop_ub;
      for (i = 0; i < loop_ub; i++) {
        b_CoefVec4_data[i] = CoefVec4_data[i] * r0->data[i];
      }

      st.site = &d_emlrtRSI;
      mfiExpPre4[j + 6 * k] = nansum(&st, b_CoefVec4_data, CoefVec4_size);
      st.site = &e_emlrtRSI;
      b_st.site = &g_emlrtRSI;
      c_st.site = &h_emlrtRSI;
      if (muDoubleScalarIsNaN(v[1])) {
        iy = 1;
        s = rtNaN;
        apnd = v[1];
        n_too_large = false;
      } else if (v[1] < 1.0) {
        iy = 0;
        s = 1.0;
        apnd = v[1];
        n_too_large = false;
      } else if (muDoubleScalarIsInf(v[1])) {
        iy = 1;
        s = rtNaN;
        apnd = v[1];
        n_too_large = !(1.0 == v[1]);
      } else {
        s = 1.0;
        ndbl = muDoubleScalarFloor((v[1] - 1.0) + 0.5);
        apnd = 1.0 + ndbl;
        cdiff = (1.0 + ndbl) - v[1];
        if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * v[1]) {
          ndbl++;
          apnd = v[1];
        } else if (cdiff > 0.0) {
          apnd = 1.0 + (ndbl - 1.0);
        } else {
          ndbl++;
        }

        n_too_large = (2.147483647E+9 < ndbl);
        if (ndbl >= 0.0) {
          iy = (int32_T)ndbl;
        } else {
          iy = 0;
        }
      }

      d_st.site = &i_emlrtRSI;
      if (!n_too_large) {
      } else {
        emlrtErrorWithMessageIdR2012b(&d_st, &c_emlrtRTEI,
          "Coder:MATLAB:pmaxsize", 0);
      }

      i = y->size[0] * y->size[1];
      y->size[0] = 1;
      y->size[1] = iy;
      emxEnsureCapacity(&c_st, (emxArray__common *)y, i, (int32_T)sizeof(real_T),
                        &emlrtRTEI);
      if (iy > 0) {
        y->data[0] = s;
        if (iy > 1) {
          y->data[iy - 1] = apnd;
          i = iy - 1;
          nm1d2 = asr_s32(i, 1U);
          d_st.site = &j_emlrtRSI;
          for (ix = 1; ix < nm1d2; ix++) {
            y->data[ix] = s + (real_T)ix;
            y->data[(iy - ix) - 1] = apnd - (real_T)ix;
          }

          if (nm1d2 << 1 == iy - 1) {
            y->data[nm1d2] = (s + apnd) / 2.0;
          } else {
            y->data[nm1d2] = s + (real_T)nm1d2;
            y->data[nm1d2 + 1] = apnd - (real_T)nm1d2;
          }
        }
      }

      st.site = &e_emlrtRSI;
      d_power(&st, Req26[j + 6 * k], y, r1);
      i = r0->size[0];
      r0->size[0] = r1->size[1];
      emxEnsureCapacity(sp, (emxArray__common *)r0, i, (int32_T)sizeof(real_T),
                        &emlrtRTEI);
      nm1d2 = r1->size[1];
      for (i = 0; i < nm1d2; i++) {
        r0->data[i] = r1->data[r1->size[0] * i];
      }

      i = r0->size[0];
      if (b_loop_ub != i) {
        emlrtSizeEqCheck1DR2012b(b_loop_ub, i, &emlrtECI, sp);
      }

      CoefVec26_size[0] = b_loop_ub;
      for (i = 0; i < b_loop_ub; i++) {
        b_CoefVec4_data[i] = CoefVec26_data[i] * r0->data[i];
      }

      st.site = &e_emlrtRSI;
      mfiExpPre26[j + 6 * k] = nansum(&st, b_CoefVec4_data, CoefVec26_size);
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

  emxFree_real_T(&r1);
  emxFree_real_T(&y);
  emxFree_real_T(&r0);
  memcpy(&b_mfiExpPre4[0], &mfiExpPre4[0], 24U * sizeof(real_T));
  rdivide(b_mfiExpPre4, kd, mfiExpPre4);
  memcpy(&b_mfiExpPre26[0], &mfiExpPre26[0], 24U * sizeof(real_T));
  rdivide(b_mfiExpPre26, kd, mfiExpPre26);
  for (i = 0; i < 4; i++) {
    for (nm1d2 = 0; nm1d2 < 6; nm1d2++) {
      c_mfiExpPre4[nm1d2 + 6 * i] = mfiExpPre4[nm1d2 + 6 * i];
      c_mfiExpPre4[nm1d2 + 6 * (i + 4)] = mfiExpPre26[nm1d2 + 6 * i];
    }
  }

  mfiExpPre_size[0] = 6;
  mfiExpPre_size[1] = 8;
  for (i = 0; i < 8; i++) {
    for (nm1d2 = 0; nm1d2 < 6; nm1d2++) {
      mfiExpPre_data[nm1d2 + 6 * i] = c_mfiExpPre4[nm1d2 + 6 * i];
    }
  }

  for (i = 0; i < 96; i++) {
    mfiExp4[i] = 0.0;
    mfiExp26[i] = 0.0;
  }

  j = 0;
  while (j < 6) {
    k = 0;
    while (k < 4) {
      i = (j << 2) + k;
      nm1d2 = (j << 2) + k;
      for (ix = 0; ix < 4; ix++) {
        mfiExp4[i + 24 * ix] = mfiExpPre4[j + 6 * k];
        mfiExp26[nm1d2 + 24 * ix] = mfiExpPre26[j + 6 * k];
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

  /* Expected MFIs */
  for (i = 0; i < 4; i++) {
    memcpy(&b_mfiExp4[i * 24], &mfiExp4[i * 24], 24U * sizeof(real_T));
    memcpy(&b_mfiExp4[i * 24 + 96], &mfiExp26[i * 24], 24U * sizeof(real_T));
  }

  mfiExp_size[0] = 24;
  mfiExp_size[1] = 8;
  for (i = 0; i < 8; i++) {
    memcpy(&mfiExp_data[i * 24], &b_mfiExp4[i * 24], 24U * sizeof(real_T));
  }

  /* Error */
  st.site = &f_emlrtRSI;
  for (i = 0; i < 96; i++) {
    c_mfiExp4[i] = mfiExp4[i] - mfiAdjMean4[i];
  }

  b_st.site = &f_emlrtRSI;
  e_power(c_mfiExp4, dv0);
  for (i = 0; i < 96; i++) {
    c_mfiExp4[i] = mfiExp26[i] - mfiAdjMean26[i];
  }

  b_st.site = &f_emlrtRSI;
  e_power(c_mfiExp4, mfiExp4);
  for (i = 0; i < 4; i++) {
    memcpy(&varargin_1[i * 24], &dv0[i * 24], 24U * sizeof(real_T));
    memcpy(&varargin_1[i * 24 + 96], &mfiExp4[i * 24], 24U * sizeof(real_T));
  }

  b_st.site = &p_emlrtRSI;
  ix = 0;
  iy = 0;
  for (i = 0; i < 8; i++) {
    nm1d2 = ix;
    ix++;
    if (!((nm1d2 + 1 >= 1) && (nm1d2 + 1 <= 192))) {
      emlrtDynamicBoundsCheckR2012b(nm1d2 + 1, 1, 192, &e_emlrtBCI, &b_st);
    }

    if (!muDoubleScalarIsNaN(varargin_1[nm1d2])) {
      s = varargin_1[nm1d2];
    } else {
      s = 0.0;
    }

    for (k = 0; k < 23; k++) {
      ix++;
      if (!((ix >= 1) && (ix <= 192))) {
        emlrtDynamicBoundsCheckR2012b(ix, 1, 192, &d_emlrtBCI, &b_st);
      }

      if (!muDoubleScalarIsNaN(varargin_1[ix - 1])) {
        s += varargin_1[ix - 1];
      }
    }

    iy++;
    if (!((iy >= 1) && (iy <= 8))) {
      emlrtDynamicBoundsCheckR2012b(iy, 1, 8, &c_emlrtBCI, &b_st);
    }

    d_y[iy - 1] = s;
  }

  *J = b_nansum(d_y);

  /* %%REMOVE */
  emlrtHeapReferenceStackLeaveFcnR2012b(sp);
}

/* End of code generation (Error.c) */
