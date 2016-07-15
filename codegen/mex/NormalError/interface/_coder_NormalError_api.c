/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_NormalError_api.c
 *
 * Code generation for function '_coder_NormalError_api'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalError.h"
#include "_coder_NormalError_api.h"
#include "NormalError_data.h"

/* Function Declarations */
static real_T (*b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[13];
static real_T (*c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *KdMat,
  const char_T *identifier))[60];
static const mxArray *c_emlrt_marshallOut(const real_T u);
static real_T (*d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[60];
static real_T (*e_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *mfiAdjMean, const char_T *identifier))[192];
static real_T (*emlrt_marshallIn(const emlrtStack *sp, const mxArray *Rtot,
  const char_T *identifier))[13];
static real_T (*f_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[192];
static real_T (*g_emlrt_marshallIn(const emlrtStack *sp, const mxArray *tnpbsa,
  const char_T *identifier))[2];
static real_T (*h_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[2];
static real_T (*i_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *meanPerCond, const char_T *identifier))[48];
static real_T (*j_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[48];
static real_T (*k_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *biCoefMat, const char_T *identifier))[900];
static real_T (*l_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[900];
static real_T (*m_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[13];
static real_T (*n_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[60];
static real_T (*o_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[192];
static real_T (*p_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[2];
static real_T (*q_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[48];
static real_T (*r_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[900];

/* Function Definitions */
static real_T (*b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[13]
{
  real_T (*y)[13];
  y = m_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}
  static real_T (*c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *KdMat,
  const char_T *identifier))[60]
{
  real_T (*y)[60];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = d_emlrt_marshallIn(sp, emlrtAlias(KdMat), &thisId);
  emlrtDestroyArray(&KdMat);
  return y;
}

static const mxArray *c_emlrt_marshallOut(const real_T u)
{
  const mxArray *y;
  const mxArray *m2;
  y = NULL;
  m2 = emlrtCreateDoubleScalar(u);
  emlrtAssign(&y, m2);
  return y;
}

static real_T (*d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[60]
{
  real_T (*y)[60];
  y = n_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}
  static real_T (*e_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *mfiAdjMean, const char_T *identifier))[192]
{
  real_T (*y)[192];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = f_emlrt_marshallIn(sp, emlrtAlias(mfiAdjMean), &thisId);
  emlrtDestroyArray(&mfiAdjMean);
  return y;
}

static real_T (*emlrt_marshallIn(const emlrtStack *sp, const mxArray *Rtot,
  const char_T *identifier))[13]
{
  real_T (*y)[13];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = b_emlrt_marshallIn(sp, emlrtAlias(Rtot), &thisId);
  emlrtDestroyArray(&Rtot);
  return y;
}
  static real_T (*f_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
  const emlrtMsgIdentifier *parentId))[192]
{
  real_T (*y)[192];
  y = o_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static real_T (*g_emlrt_marshallIn(const emlrtStack *sp, const mxArray *tnpbsa,
  const char_T *identifier))[2]
{
  real_T (*y)[2];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = h_emlrt_marshallIn(sp, emlrtAlias(tnpbsa), &thisId);
  emlrtDestroyArray(&tnpbsa);
  return y;
}
  static real_T (*h_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
  const emlrtMsgIdentifier *parentId))[2]
{
  real_T (*y)[2];
  y = p_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static real_T (*i_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *meanPerCond, const char_T *identifier))[48]
{
  real_T (*y)[48];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = j_emlrt_marshallIn(sp, emlrtAlias(meanPerCond), &thisId);
  emlrtDestroyArray(&meanPerCond);
  return y;
}
  static real_T (*j_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
  const emlrtMsgIdentifier *parentId))[48]
{
  real_T (*y)[48];
  y = q_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static real_T (*k_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *biCoefMat, const char_T *identifier))[900]
{
  real_T (*y)[900];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = l_emlrt_marshallIn(sp, emlrtAlias(biCoefMat), &thisId);
  emlrtDestroyArray(&biCoefMat);
  return y;
}
  static real_T (*l_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u,
  const emlrtMsgIdentifier *parentId))[900]
{
  real_T (*y)[900];
  y = r_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static real_T (*m_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[13]
{
  real_T (*ret)[13];
  static const int32_T dims[2] = { 1, 13 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[13])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}
  static real_T (*n_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[60]
{
  real_T (*ret)[60];
  static const int32_T dims[2] = { 6, 10 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[60])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

static real_T (*o_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[192]
{
  real_T (*ret)[192];
  static const int32_T dims[2] = { 24, 8 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[192])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}
  static real_T (*p_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[2]
{
  real_T (*ret)[2];
  static const int32_T dims[1] = { 2 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 1U, dims);
  ret = (real_T (*)[2])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

static real_T (*q_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[48]
{
  real_T (*ret)[48];
  static const int32_T dims[2] = { 24, 2 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[48])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}
  static real_T (*r_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[900]
{
  real_T (*ret)[900];
  static const int32_T dims[2] = { 30, 30 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[900])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

void NormalError_api(const mxArray * const prhs[6], const mxArray *plhs[1])
{
  real_T (*Rtot)[13];
  real_T (*KdMat)[60];
  real_T (*mfiAdjMean)[192];
  real_T (*tnpbsa)[2];
  real_T (*meanPerCond)[48];
  real_T (*biCoefMat)[900];
  real_T logSqrErr;
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;

  /* Marshall function inputs */
  Rtot = emlrt_marshallIn(&st, emlrtAlias(prhs[0]), "Rtot");
  KdMat = c_emlrt_marshallIn(&st, emlrtAlias(prhs[1]), "KdMat");
  mfiAdjMean = e_emlrt_marshallIn(&st, emlrtAlias(prhs[2]), "mfiAdjMean");
  tnpbsa = g_emlrt_marshallIn(&st, emlrtAlias(prhs[3]), "tnpbsa");
  meanPerCond = i_emlrt_marshallIn(&st, emlrtAlias(prhs[4]), "meanPerCond");
  biCoefMat = k_emlrt_marshallIn(&st, emlrtAlias(prhs[5]), "biCoefMat");

  /* Invoke the target function */
  logSqrErr = NormalError(&st, *Rtot, *KdMat, *mfiAdjMean, *tnpbsa, *meanPerCond,
    *biCoefMat);

  /* Marshall function outputs */
  plhs[0] = c_emlrt_marshallOut(logSqrErr);
}

/* End of code generation (_coder_NormalError_api.c) */
