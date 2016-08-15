/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_PROPRND_api.c
 *
 * Code generation for function '_coder_PROPRND_api'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "_coder_PROPRND_api.h"
#include "PROPRND_data.h"

/* Function Declarations */
static real_T (*b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[12];
static real_T c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *lbR, const
  char_T *identifier);
static real_T d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId);
static real_T (*e_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[12];
static real_T (*emlrt_marshallIn(const emlrtStack *sp, const mxArray *current,
  const char_T *identifier))[12];
static const mxArray *emlrt_marshallOut(const real_T u[12]);
static real_T f_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId);

/* Function Definitions */
static real_T (*b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[12]
{
  real_T (*y)[12];
  y = e_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}
  static real_T c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *lbR,
  const char_T *identifier)
{
  real_T y;
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = d_emlrt_marshallIn(sp, emlrtAlias(lbR), &thisId);
  emlrtDestroyArray(&lbR);
  return y;
}

static real_T d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId)
{
  real_T y;
  y = f_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static real_T (*e_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[12]
{
  real_T (*ret)[12];
  static const int32_T dims[2] = { 1, 12 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[12])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}
  static real_T (*emlrt_marshallIn(const emlrtStack *sp, const mxArray *current,
  const char_T *identifier))[12]
{
  real_T (*y)[12];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = b_emlrt_marshallIn(sp, emlrtAlias(current), &thisId);
  emlrtDestroyArray(&current);
  return y;
}

static const mxArray *emlrt_marshallOut(const real_T u[12])
{
  const mxArray *y;
  const mxArray *m0;
  static const int32_T iv0[2] = { 0, 0 };

  static const int32_T iv1[2] = { 1, 12 };

  y = NULL;
  m0 = emlrtCreateNumericArray(2, iv0, mxDOUBLE_CLASS, mxREAL);
  mxSetData((mxArray *)m0, (void *)u);
  emlrtSetDimensions((mxArray *)m0, iv1, 2);
  emlrtAssign(&y, m0);
  return y;
}

static real_T f_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId)
{
  real_T ret;
  static const int32_T dims = 0;
  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 0U, &dims);
  ret = *(real_T *)mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

void PROPRND_api(const mxArray * const prhs[15], const mxArray *plhs[1])
{
  real_T (*next)[12];
  real_T (*current)[12];
  real_T lbR;
  real_T ubR;
  real_T lbKx;
  real_T ubKx;
  real_T lbc;
  real_T ubc;
  real_T lbv;
  real_T ubv;
  real_T lbsigma;
  real_T ubsigma;
  real_T stdR;
  real_T stdKx;
  real_T stdc;
  real_T stdsigma;
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;
  next = (real_T (*)[12])mxMalloc(sizeof(real_T [12]));

  /* Marshall function inputs */
  current = emlrt_marshallIn(&st, emlrtAlias(prhs[0]), "current");
  lbR = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[1]), "lbR");
  ubR = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[2]), "ubR");
  lbKx = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[3]), "lbKx");
  ubKx = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[4]), "ubKx");
  lbc = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[5]), "lbc");
  ubc = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[6]), "ubc");
  lbv = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[7]), "lbv");
  ubv = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[8]), "ubv");
  lbsigma = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[9]), "lbsigma");
  ubsigma = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[10]), "ubsigma");
  stdR = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[11]), "stdR");
  stdKx = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[12]), "stdKx");
  stdc = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[13]), "stdc");
  stdsigma = c_emlrt_marshallIn(&st, emlrtAliasP(prhs[14]), "stdsigma");

  /* Invoke the target function */
  PROPRND(&st, *current, lbR, ubR, lbKx, ubKx, lbc, ubc, lbv, ubv, lbsigma,
          ubsigma, stdR, stdKx, stdc, stdsigma, *next);

  /* Marshall function outputs */
  plhs[0] = emlrt_marshallOut(*next);
}

/* End of code generation (_coder_PROPRND_api.c) */
