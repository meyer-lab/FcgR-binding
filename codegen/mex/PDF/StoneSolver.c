/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * StoneSolver.c
 *
 * Code generation for function 'StoneSolver'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "StoneSolver.h"
#include "error1.h"
#include "power.h"
#include "PDF_data.h"

/* Variable Definitions */
static emlrtRSInfo g_emlrtRSI = { 6, "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m" };

static emlrtRSInfo h_emlrtRSI = { 15, "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m" };

static emlrtRSInfo i_emlrtRSI = { 26, "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m" };

static emlrtRSInfo j_emlrtRSI = { 13, "log10",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\elfun\\log10.m"
};

static emlrtRSInfo k_emlrtRSI = { 21, "colon",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\ops\\colon.m" };

static emlrtRSInfo q_emlrtRSI = { 13, "sum",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\datafun\\sum.m"
};

static emlrtDCInfo emlrtDCI = { 15, 30, "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m", 1 };

static emlrtBCInfo d_emlrtBCI = { 1, 26, 15, 30, "biCoefMat", "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m", 0 };

static emlrtDCInfo b_emlrtDCI = { 15, 34, "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m", 1 };

static emlrtBCInfo e_emlrtBCI = { 1, 26, 15, 34, "biCoefMat", "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m", 0 };

static emlrtECInfo b_emlrtECI = { 2, 15, 20, "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m" };

static emlrtECInfo c_emlrtECI = { 2, 15, 13, "StoneSolver",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\StoneSolver.m" };

static emlrtRTEInfo b_emlrtRTEI = { 19, 15, "sumprod",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\datafun\\private\\sumprod.m"
};

static emlrtRTEInfo c_emlrtRTEI = { 39, 9, "sumprod",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\eml\\lib\\matlab\\datafun\\private\\sumprod.m"
};

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

real_T StoneSolver(const emlrtStack *sp, real_T Rtot, real_T Kx, real_T v,
                   real_T Kd, real_T L0, const real_T biCoefMat[676])
{
  real_T L;
  real_T viLikdi;
  real_T a;
  real_T b;
  real_T x;
  real_T bVal;
  real_T cVal;
  real_T Req;
  int32_T loop_ub;
  int32_T cdiff;
  int32_T x_size[2];
  real_T x_data[26];
  int32_T ndbl;
  int32_T apnd;
  real_T y_data[26];
  int32_T k;
  real_T b_y_data[26];
  int32_T y_size[2];
  int32_T b_y_size[2];
  int32_T b_x[2];
  int32_T y[2];
  int32_T c_x[2];
  int32_T iv1[2];
  boolean_T p;
  boolean_T b_p;
  int32_T exitg1;
  emlrtStack st;
  emlrtStack b_st;
  emlrtStack c_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;
  c_st.prev = &b_st;
  c_st.tls = b_st.tls;

  /* Using the information given, finds the sum L presented in Equation 7 */
  /* in Stone. In this context, all inputs save biCoefMat are scalars. */
  /* Solve for Req, as described in Equation 2 in Stone */
  st.site = &g_emlrtRSI;

  /* -------------------------------------------------------------------------- */
  /* %%This function returns the point at which function fun equals zero */
  /* %%using the bisection algorithm. The closest a and b will converge to */
  /* %%in the algorithm is a distance 1e-12 apart. */
  viLikdi = v * L0 / Kd;
  a = -20.0;
  b_st.site = &i_emlrtRSI;
  if (Rtot < 0.0) {
    c_st.site = &j_emlrtRSI;
    error(&c_st);
  }

  b = muDoubleScalarLog10(Rtot);

  /* -------------------------------------------------------------------------- */
  x = muDoubleScalarPower(10.0, b);
  bVal = Rtot - x * (1.0 + viLikdi * muDoubleScalarPower(1.0 + Kx * x, v - 1.0));

  /* -------------------------------------------------------------------------- */
  cVal = Rtot - 1.0000000000000001E-20 * (1.0 + viLikdi * muDoubleScalarPower
    (1.0 + Kx * 1.0000000000000001E-20, v - 1.0));

  /*  Is there no root within the interval? */
  if (bVal * cVal > 0.0) {
    Req = 1000.0;
  } else {
    /* In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin */
    /* with; only implemented for MATLAB Coder */
    Req = 1000.0;

    /* Commence algorithm */
    while ((b - a > 0.0001) || (muDoubleScalarAbs(cVal) > 0.0001)) {
      Req = (a + b) / 2.0;

      /* -------------------------------------------------------------------------- */
      x = muDoubleScalarPower(10.0, Req);
      cVal = Rtot - x * (1.0 + viLikdi * muDoubleScalarPower(1.0 + Kx * x, v -
        1.0));
      if (cVal * bVal >= 0.0) {
        b = Req;
        bVal = cVal;
      } else {
        a = Req;
      }

      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(&st);
      }
    }
  }

  /* Check for error output from ReqFuncSolver */
  if (Req == 1000.0) {
    L = -1.0;
  } else {
    /* Convert from logarithmic scale */
    Req = muDoubleScalarPower(10.0, Req);
    if (1.0 > v) {
      loop_ub = 0;
    } else {
      if (v != (int32_T)muDoubleScalarFloor(v)) {
        emlrtIntegerCheckR2012b(v, &emlrtDCI, sp);
      }

      loop_ub = (int32_T)v;
      if (!((loop_ub >= 1) && (loop_ub <= 26))) {
        emlrtDynamicBoundsCheckR2012b(loop_ub, 1, 26, &d_emlrtBCI, sp);
      }
    }

    if (v != (int32_T)muDoubleScalarFloor(v)) {
      emlrtIntegerCheckR2012b(v, &b_emlrtDCI, sp);
    }

    cdiff = (int32_T)v;
    if (!((cdiff >= 1) && (cdiff <= 26))) {
      emlrtDynamicBoundsCheckR2012b(cdiff, 1, 26, &e_emlrtBCI, sp);
    }

    x_size[0] = 1;
    x_size[1] = loop_ub;
    for (cdiff = 0; cdiff < loop_ub; cdiff++) {
      x_data[cdiff] = biCoefMat[cdiff + 26 * ((int32_T)v - 1)];
    }

    st.site = &h_emlrtRSI;
    b_st.site = &k_emlrtRSI;
    ndbl = (int32_T)muDoubleScalarFloor((v - 1.0) + 0.5);
    apnd = ndbl + 1;
    cdiff = (ndbl - (int32_T)v) + 1;
    if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * (real_T)(int32_T)v)
    {
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
        cdiff = ndbl - 1;
        cdiff = asr_s32(cdiff, 1U);
        for (k = 1; k < cdiff; k++) {
          y_data[k] = 1.0 + (real_T)k;
          y_data[(ndbl - k) - 1] = apnd - k;
        }

        if (cdiff << 1 == ndbl - 1) {
          y_data[cdiff] = (1.0 + (real_T)apnd) / 2.0;
        } else {
          y_data[cdiff] = 1.0 + (real_T)cdiff;
          y_data[cdiff + 1] = apnd - cdiff;
        }
      }
    }

    y_size[0] = 1;
    y_size[1] = ndbl;
    for (cdiff = 0; cdiff < ndbl; cdiff++) {
      b_y_data[cdiff] = y_data[cdiff] - 1.0;
    }

    st.site = &h_emlrtRSI;
    power(&st, Kx, b_y_data, y_size, y_data, b_y_size);
    for (cdiff = 0; cdiff < 2; cdiff++) {
      b_x[cdiff] = x_size[cdiff];
      y[cdiff] = b_y_size[cdiff];
    }

    if ((b_x[0] != y[0]) || (b_x[1] != y[1])) {
      emlrtSizeEqCheckNDR2012b(&b_x[0], &y[0], &b_emlrtECI, sp);
    }

    x = L0 / Kd;
    x_size[0] = 1;
    for (cdiff = 0; cdiff < loop_ub; cdiff++) {
      x_data[cdiff] = x * (x_data[cdiff] * y_data[cdiff]);
    }

    st.site = &h_emlrtRSI;
    b_st.site = &k_emlrtRSI;
    ndbl = (int32_T)muDoubleScalarFloor((v - 1.0) + 0.5);
    apnd = ndbl + 1;
    cdiff = (ndbl - (int32_T)v) + 1;
    if (muDoubleScalarAbs(cdiff) < 4.4408920985006262E-16 * (real_T)(int32_T)v)
    {
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
        cdiff = ndbl - 1;
        cdiff = asr_s32(cdiff, 1U);
        for (k = 1; k < cdiff; k++) {
          y_data[k] = 1.0 + (real_T)k;
          y_data[(ndbl - k) - 1] = apnd - k;
        }

        if (cdiff << 1 == ndbl - 1) {
          y_data[cdiff] = (1.0 + (real_T)apnd) / 2.0;
        } else {
          y_data[cdiff] = 1.0 + (real_T)cdiff;
          y_data[cdiff + 1] = apnd - cdiff;
        }
      }
    }

    st.site = &h_emlrtRSI;
    power(&st, Req, y_data, b_y_size, b_y_data, y_size);
    for (cdiff = 0; cdiff < 2; cdiff++) {
      c_x[cdiff] = x_size[cdiff];
      iv1[cdiff] = y_size[cdiff];
    }

    if ((c_x[0] != iv1[0]) || (c_x[1] != iv1[1])) {
      emlrtSizeEqCheckNDR2012b(&c_x[0], &iv1[0], &c_emlrtECI, sp);
    }

    st.site = &h_emlrtRSI;
    x_size[0] = 1;
    for (cdiff = 0; cdiff < loop_ub; cdiff++) {
      x_data[cdiff] *= b_y_data[cdiff];
    }

    b_st.site = &q_emlrtRSI;
    if ((loop_ub == 1) || (loop_ub != 1)) {
      p = true;
    } else {
      p = false;
    }

    if (p) {
    } else {
      emlrtErrorWithMessageIdR2012b(&b_st, &b_emlrtRTEI,
        "Coder:toolbox:autoDimIncompatibility", 0);
    }

    p = false;
    b_p = false;
    k = 0;
    do {
      exitg1 = 0;
      if (k < 2) {
        if (x_size[k] != 0) {
          exitg1 = 1;
        } else {
          k++;
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
      emlrtErrorWithMessageIdR2012b(&b_st, &c_emlrtRTEI,
        "Coder:toolbox:UnsupportedSpecialEmpty", 0);
    }

    if (loop_ub == 0) {
      L = 0.0;
    } else {
      L = x_data[0];
      for (k = 2; k <= loop_ub; k++) {
        L += x_data[k - 1];
      }
    }
  }

  return L;
}

/* End of code generation (StoneSolver.c) */
