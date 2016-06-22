/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: Error.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 22-Jun-2016 09:56:36
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "Error.h"
#include "nansum.h"
#include "PDF_emxutil.h"
#include "power.h"
#include "PDF_rtwutil.h"

/* Function Definitions */

/*
 * Arguments    : double Rtot[7]
 *                const double kd[24]
 *                const double mfiAdjMean4[96]
 *                const double mfiAdjMean26[96]
 *                const double v[2]
 *                const double biCoefMat[676]
 *                const double tnpbsa[2]
 *                double *J
 *                double mfiExp_data[]
 *                int mfiExp_size[2]
 *                double mfiExpPre_data[]
 *                int mfiExpPre_size[2]
 * Return Type  : void
 */
void Error(double Rtot[7], const double kd[24], const double mfiAdjMean4[96],
           const double mfiAdjMean26[96], const double v[2], const double
           biCoefMat[676], const double tnpbsa[2], double *J, double
           mfiExp_data[], int mfiExp_size[2], double mfiExpPre_data[], int
           mfiExpPre_size[2])
{
  double b_Rtot[7];
  int i;
  double Req4[24];
  double Req26[24];
  int j;
  int k;
  double b_Req4[24];
  double b_Req26[24];
  int loop_ub;
  int iy;
  double s;
  double apnd;
  double ndbl;
  double cdiff;
  emxArray_real_T *y;
  int nm1d2;
  emxArray_real_T *b_y;
  int b_loop_ub;
  emxArray_real_T *r0;
  double CoefVec4_data[26];
  emxArray_real_T *c_y;
  double CoefVec26_data[26];
  double mfiExpPre4[24];
  double mfiExpPre26[24];
  emxArray_real_T *r1;
  int ix;
  double b_CoefVec4_data[26];
  int CoefVec4_size[1];
  int CoefVec26_size[1];
  double b_mfiExpPre4[48];
  double mfiExp4[96];
  double mfiExp26[96];
  double b_mfiExp4[192];
  double d_y[96];
  double varargin_1[192];
  double e_y[8];
  for (i = 0; i < 7; i++) {
    b_Rtot[i] = Rtot[i];
  }

  power(b_Rtot, Rtot);

  /* Preallocating space for the Req values (according to Stone et al.) for */
  /* each combination of IgG and FcgR per flavor of TNP-X-BSA. */
  /*      ReqFunc = @(Reqi, R, kdi, Li, vi) R - Reqi*(1+vi*Li/kdi*(1+kx*Reqi)^(vi-1)); */
  /* Finding Req values by means of bisection algorithm */
  for (j = 0; j < 6; j++) {
    for (k = 0; k < 4; k++) {
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
    }
  }

  /* Preventing errors in global optimization due to failure of the */
  /* above local solver */
  memcpy(&b_Req4[0], &Req4[0], 24U * sizeof(double));
  b_power(b_Req4, Req4);
  memcpy(&b_Req26[0], &Req26[0], 24U * sizeof(double));
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
    loop_ub = (int)v[0];
  }

  if (rtIsNaN(v[0])) {
    iy = 1;
    s = rtNaN;
    apnd = v[0];
  } else if (v[0] < 1.0) {
    iy = 0;
    s = 1.0;
    apnd = v[0];
  } else if (rtIsInf(v[0])) {
    iy = 1;
    s = rtNaN;
    apnd = v[0];
  } else {
    s = 1.0;
    ndbl = floor((v[0] - 1.0) + 0.5);
    apnd = 1.0 + ndbl;
    cdiff = (1.0 + ndbl) - v[0];
    if (fabs(cdiff) < 4.4408920985006262E-16 * v[0]) {
      ndbl++;
      apnd = v[0];
    } else if (cdiff > 0.0) {
      apnd = 1.0 + (ndbl - 1.0);
    } else {
      ndbl++;
    }

    if (ndbl >= 0.0) {
      iy = (int)ndbl;
    } else {
      iy = 0;
    }
  }

  emxInit_real_T1(&y, 2);
  i = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = iy;
  emxEnsureCapacity((emxArray__common *)y, i, (int)sizeof(double));
  if (iy > 0) {
    y->data[0] = s;
    if (iy > 1) {
      y->data[iy - 1] = apnd;
      i = iy - 1;
      nm1d2 = i / 2;
      for (k = 1; k < nm1d2; k++) {
        y->data[k] = s + (double)k;
        y->data[(iy - k) - 1] = apnd - (double)k;
      }

      if (nm1d2 << 1 == iy - 1) {
        y->data[nm1d2] = (s + apnd) / 2.0;
      } else {
        y->data[nm1d2] = s + (double)nm1d2;
        y->data[nm1d2 + 1] = apnd - (double)nm1d2;
      }
    }
  }

  emxInit_real_T(&b_y, 1);
  i = b_y->size[0];
  b_y->size[0] = y->size[1];
  emxEnsureCapacity((emxArray__common *)b_y, i, (int)sizeof(double));
  b_loop_ub = y->size[1];
  for (i = 0; i < b_loop_ub; i++) {
    b_y->data[i] = y->data[y->size[0] * i] - 1.0;
  }

  emxInit_real_T(&r0, 1);
  c_power(Rtot[0], b_y, r0);
  emxFree_real_T(&b_y);
  for (i = 0; i < loop_ub; i++) {
    CoefVec4_data[i] = biCoefMat[i + 26 * ((int)v[0] - 1)] * r0->data[i] *
      tnpbsa[0];
  }

  if (1.0 > v[1]) {
    b_loop_ub = 0;
  } else {
    b_loop_ub = (int)v[1];
  }

  if (rtIsNaN(v[1])) {
    iy = 1;
    s = rtNaN;
    apnd = v[1];
  } else if (v[1] < 1.0) {
    iy = 0;
    s = 1.0;
    apnd = v[1];
  } else if (rtIsInf(v[1])) {
    iy = 1;
    s = rtNaN;
    apnd = v[1];
  } else {
    s = 1.0;
    ndbl = floor((v[1] - 1.0) + 0.5);
    apnd = 1.0 + ndbl;
    cdiff = (1.0 + ndbl) - v[1];
    if (fabs(cdiff) < 4.4408920985006262E-16 * v[1]) {
      ndbl++;
      apnd = v[1];
    } else if (cdiff > 0.0) {
      apnd = 1.0 + (ndbl - 1.0);
    } else {
      ndbl++;
    }

    if (ndbl >= 0.0) {
      iy = (int)ndbl;
    } else {
      iy = 0;
    }
  }

  i = y->size[0] * y->size[1];
  y->size[0] = 1;
  y->size[1] = iy;
  emxEnsureCapacity((emxArray__common *)y, i, (int)sizeof(double));
  if (iy > 0) {
    y->data[0] = s;
    if (iy > 1) {
      y->data[iy - 1] = apnd;
      i = iy - 1;
      nm1d2 = i / 2;
      for (k = 1; k < nm1d2; k++) {
        y->data[k] = s + (double)k;
        y->data[(iy - k) - 1] = apnd - (double)k;
      }

      if (nm1d2 << 1 == iy - 1) {
        y->data[nm1d2] = (s + apnd) / 2.0;
      } else {
        y->data[nm1d2] = s + (double)nm1d2;
        y->data[nm1d2 + 1] = apnd - (double)nm1d2;
      }
    }
  }

  emxInit_real_T(&c_y, 1);
  i = c_y->size[0];
  c_y->size[0] = y->size[1];
  emxEnsureCapacity((emxArray__common *)c_y, i, (int)sizeof(double));
  nm1d2 = y->size[1];
  for (i = 0; i < nm1d2; i++) {
    c_y->data[i] = y->data[y->size[0] * i] - 1.0;
  }

  c_power(Rtot[0], c_y, r0);
  emxFree_real_T(&c_y);
  for (i = 0; i < b_loop_ub; i++) {
    CoefVec26_data[i] = biCoefMat[i + 26 * ((int)v[1] - 1)] * r0->data[i] *
      tnpbsa[1];
  }

  /* Creating matrix of expected MFIs; takes a few steps to do so */
  for (i = 0; i < 24; i++) {
    mfiExpPre4[i] = 0.0;
    mfiExpPre26[i] = 0.0;
  }

  emxInit_real_T1(&r1, 2);
  for (j = 0; j < 6; j++) {
    for (k = 0; k < 4; k++) {
      if (rtIsNaN(v[0])) {
        iy = 1;
        s = rtNaN;
        apnd = v[0];
      } else if (v[0] < 1.0) {
        iy = 0;
        s = 1.0;
        apnd = v[0];
      } else if (rtIsInf(v[0])) {
        iy = 1;
        s = rtNaN;
        apnd = v[0];
      } else {
        s = 1.0;
        ndbl = floor((v[0] - 1.0) + 0.5);
        apnd = 1.0 + ndbl;
        cdiff = (1.0 + ndbl) - v[0];
        if (fabs(cdiff) < 4.4408920985006262E-16 * v[0]) {
          ndbl++;
          apnd = v[0];
        } else if (cdiff > 0.0) {
          apnd = 1.0 + (ndbl - 1.0);
        } else {
          ndbl++;
        }

        if (ndbl >= 0.0) {
          iy = (int)ndbl;
        } else {
          iy = 0;
        }
      }

      i = y->size[0] * y->size[1];
      y->size[0] = 1;
      y->size[1] = iy;
      emxEnsureCapacity((emxArray__common *)y, i, (int)sizeof(double));
      if (iy > 0) {
        y->data[0] = s;
        if (iy > 1) {
          y->data[iy - 1] = apnd;
          i = iy - 1;
          nm1d2 = i / 2;
          for (ix = 1; ix < nm1d2; ix++) {
            y->data[ix] = s + (double)ix;
            y->data[(iy - ix) - 1] = apnd - (double)ix;
          }

          if (nm1d2 << 1 == iy - 1) {
            y->data[nm1d2] = (s + apnd) / 2.0;
          } else {
            y->data[nm1d2] = s + (double)nm1d2;
            y->data[nm1d2 + 1] = apnd - (double)nm1d2;
          }
        }
      }

      d_power(Req4[j + 6 * k], y, r1);
      i = r0->size[0];
      r0->size[0] = r1->size[1];
      emxEnsureCapacity((emxArray__common *)r0, i, (int)sizeof(double));
      nm1d2 = r1->size[1];
      for (i = 0; i < nm1d2; i++) {
        r0->data[i] = r1->data[r1->size[0] * i];
      }

      CoefVec4_size[0] = loop_ub;
      for (i = 0; i < loop_ub; i++) {
        b_CoefVec4_data[i] = CoefVec4_data[i] * r0->data[i];
      }

      mfiExpPre4[j + 6 * k] = nansum(b_CoefVec4_data, CoefVec4_size);
      if (rtIsNaN(v[1])) {
        iy = 1;
        s = rtNaN;
        apnd = v[1];
      } else if (v[1] < 1.0) {
        iy = 0;
        s = 1.0;
        apnd = v[1];
      } else if (rtIsInf(v[1])) {
        iy = 1;
        s = rtNaN;
        apnd = v[1];
      } else {
        s = 1.0;
        ndbl = floor((v[1] - 1.0) + 0.5);
        apnd = 1.0 + ndbl;
        cdiff = (1.0 + ndbl) - v[1];
        if (fabs(cdiff) < 4.4408920985006262E-16 * v[1]) {
          ndbl++;
          apnd = v[1];
        } else if (cdiff > 0.0) {
          apnd = 1.0 + (ndbl - 1.0);
        } else {
          ndbl++;
        }

        if (ndbl >= 0.0) {
          iy = (int)ndbl;
        } else {
          iy = 0;
        }
      }

      i = y->size[0] * y->size[1];
      y->size[0] = 1;
      y->size[1] = iy;
      emxEnsureCapacity((emxArray__common *)y, i, (int)sizeof(double));
      if (iy > 0) {
        y->data[0] = s;
        if (iy > 1) {
          y->data[iy - 1] = apnd;
          i = iy - 1;
          nm1d2 = i / 2;
          for (ix = 1; ix < nm1d2; ix++) {
            y->data[ix] = s + (double)ix;
            y->data[(iy - ix) - 1] = apnd - (double)ix;
          }

          if (nm1d2 << 1 == iy - 1) {
            y->data[nm1d2] = (s + apnd) / 2.0;
          } else {
            y->data[nm1d2] = s + (double)nm1d2;
            y->data[nm1d2 + 1] = apnd - (double)nm1d2;
          }
        }
      }

      d_power(Req26[j + 6 * k], y, r1);
      i = r0->size[0];
      r0->size[0] = r1->size[1];
      emxEnsureCapacity((emxArray__common *)r0, i, (int)sizeof(double));
      nm1d2 = r1->size[1];
      for (i = 0; i < nm1d2; i++) {
        r0->data[i] = r1->data[r1->size[0] * i];
      }

      CoefVec26_size[0] = b_loop_ub;
      for (i = 0; i < b_loop_ub; i++) {
        b_CoefVec4_data[i] = CoefVec26_data[i] * r0->data[i];
      }

      mfiExpPre26[j + 6 * k] = nansum(b_CoefVec4_data, CoefVec26_size);
    }
  }

  emxFree_real_T(&r1);
  emxFree_real_T(&y);
  emxFree_real_T(&r0);
  for (i = 0; i < 24; i++) {
    mfiExpPre4[i] /= kd[i];
    mfiExpPre26[i] /= kd[i];
  }

  for (i = 0; i < 4; i++) {
    for (nm1d2 = 0; nm1d2 < 6; nm1d2++) {
      b_mfiExpPre4[nm1d2 + 6 * i] = mfiExpPre4[nm1d2 + 6 * i];
      b_mfiExpPre4[nm1d2 + 6 * (i + 4)] = mfiExpPre26[nm1d2 + 6 * i];
    }
  }

  mfiExpPre_size[0] = 6;
  mfiExpPre_size[1] = 8;
  for (i = 0; i < 8; i++) {
    for (nm1d2 = 0; nm1d2 < 6; nm1d2++) {
      mfiExpPre_data[nm1d2 + 6 * i] = b_mfiExpPre4[nm1d2 + 6 * i];
    }
  }

  for (j = 0; j < 6; j++) {
    for (k = 0; k < 4; k++) {
      i = (j << 2) + k;
      nm1d2 = (j << 2) + k;
      for (ix = 0; ix < 4; ix++) {
        mfiExp4[i + 24 * ix] = mfiExpPre4[j + 6 * k];
        mfiExp26[nm1d2 + 24 * ix] = mfiExpPre26[j + 6 * k];
      }
    }
  }

  /* Expected MFIs */
  for (i = 0; i < 4; i++) {
    memcpy(&b_mfiExp4[i * 24], &mfiExp4[i * 24], 24U * sizeof(double));
    memcpy(&b_mfiExp4[i * 24 + 96], &mfiExp26[i * 24], 24U * sizeof(double));
  }

  mfiExp_size[0] = 24;
  mfiExp_size[1] = 8;
  for (i = 0; i < 8; i++) {
    memcpy(&mfiExp_data[i * 24], &b_mfiExp4[i * 24], 24U * sizeof(double));
  }

  /* Error */
  for (k = 0; k < 96; k++) {
    d_y[k] = rt_powd_snf(mfiExp4[k] - mfiAdjMean4[k], 2.0);
    mfiExp26[k] -= mfiAdjMean26[k];
  }

  for (k = 0; k < 96; k++) {
    mfiExp4[k] = rt_powd_snf(mfiExp26[k], 2.0);
  }

  for (i = 0; i < 4; i++) {
    memcpy(&varargin_1[i * 24], &d_y[i * 24], 24U * sizeof(double));
    memcpy(&varargin_1[i * 24 + 96], &mfiExp4[i * 24], 24U * sizeof(double));
  }

  ix = -1;
  iy = -1;
  for (i = 0; i < 8; i++) {
    nm1d2 = ix + 1;
    ix++;
    if (!rtIsNaN(varargin_1[nm1d2])) {
      s = varargin_1[nm1d2];
    } else {
      s = 0.0;
    }

    for (k = 0; k < 23; k++) {
      ix++;
      if (!rtIsNaN(varargin_1[ix])) {
        s += varargin_1[ix];
      }
    }

    iy++;
    e_y[iy] = s;
  }

  *J = 0.0;
  for (k = 0; k < 8; k++) {
    if (!rtIsNaN(e_y[k])) {
      *J += e_y[k];
    }
  }

  /* %%REMOVE */
}

/*
 * File trailer for Error.c
 *
 * [EOF]
 */
