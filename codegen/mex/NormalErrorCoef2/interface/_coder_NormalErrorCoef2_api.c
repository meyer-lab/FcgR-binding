/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_NormalErrorCoef2_api.c
 *
 * Code generation for function '_coder_NormalErrorCoef2_api'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef2.h"
#include "_coder_NormalErrorCoef2_api.h"
#include "NormalErrorCoef2_data.h"

/* Function Declarations */
static real_T (*b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[12];
static real_T (*c_emlrt_marshallIn(const emlrtStack *sp, const mxArray *KdMat,
  const char_T *identifier))[60];
static real_T (*d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[60];
static real_T (*e_emlrt_marshallIn(const emlrtStack *sp, const mxArray
  *mfiAdjMean, const char_T *identifier))[192];
static real_T (*emlrt_marshallIn(const emlrtStack *sp, const mxArray *Rtot,
  const char_T *identifier))[12];
static const mxArray *emlrt_marshallOut(const real_T u);
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
static real_T m_emlrt_marshallIn(const emlrtStack *sp, const mxArray *whichR,
  const char_T *identifier);
static real_T n_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId);
static real_T (*o_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[12];
static real_T (*p_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[60];
static real_T (*q_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[192];
static real_T (*r_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[2];
static real_T (*s_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[48];
static real_T (*t_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[900];
static real_T u_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId);

/* Function Definitions */
static real_T (*b_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[12]
{
  real_T (*y)[12];
  y = o_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
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

static real_T (*d_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[60]
{
  real_T (*y)[60];
  y = p_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
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
  const char_T *identifier))[12]
{
  real_T (*y)[12];
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = b_emlrt_marshallIn(sp, emlrtAlias(Rtot), &thisId);
  emlrtDestroyArray(&Rtot);
  return y;
}
  static const mxArray *emlrt_marshallOut(const real_T u)
{
  const mxArray *y;
  const mxArray *m0;
  y = NULL;
  m0 = emlrtCreateDoubleScalar(u);
  emlrtAssign(&y, m0);
  return y;
}

static real_T (*f_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[192]
{
  real_T (*y)[192];
  y = q_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
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

static real_T (*h_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[2]
{
  real_T (*y)[2];
  y = r_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
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

static real_T (*j_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[48]
{
  real_T (*y)[48];
  y = s_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
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

static real_T (*l_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId))[900]
{
  real_T (*y)[900];
  y = t_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}
  static real_T m_emlrt_marshallIn(const emlrtStack *sp, const mxArray *whichR,
  const char_T *identifier)
{
  real_T y;
  emlrtMsgIdentifier thisId;
  thisId.fIdentifier = identifier;
  thisId.fParent = NULL;
  thisId.bParentIsCell = false;
  y = n_emlrt_marshallIn(sp, emlrtAlias(whichR), &thisId);
  emlrtDestroyArray(&whichR);
  return y;
}

static real_T n_emlrt_marshallIn(const emlrtStack *sp, const mxArray *u, const
  emlrtMsgIdentifier *parentId)
{
  real_T y;
  y = u_emlrt_marshallIn(sp, emlrtAlias(u), parentId);
  emlrtDestroyArray(&u);
  return y;
}

static real_T (*o_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[12]
{
  real_T (*ret)[12];
  static const int32_T dims[2] = { 1, 12 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[12])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}
  static real_T (*p_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[60]
{
  real_T (*ret)[60];
  static const int32_T dims[2] = { 6, 10 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[60])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

static real_T (*q_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[192]
{
  real_T (*ret)[192];
  static const int32_T dims[2] = { 24, 8 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[192])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}
  static real_T (*r_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[2]
{
  real_T (*ret)[2];
  static const int32_T dims[1] = { 2 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 1U, dims);
  ret = (real_T (*)[2])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

static real_T (*s_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[48]
{
  real_T (*ret)[48];
  static const int32_T dims[2] = { 24, 2 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[48])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}
  static real_T (*t_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src,
  const emlrtMsgIdentifier *msgId))[900]
{
  real_T (*ret)[900];
  static const int32_T dims[2] = { 30, 30 };

  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 2U, dims);
  ret = (real_T (*)[900])mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

static real_T u_emlrt_marshallIn(const emlrtStack *sp, const mxArray *src, const
  emlrtMsgIdentifier *msgId)
{
  real_T ret;
  static const int32_T dims = 0;
  emlrtCheckBuiltInR2012b(sp, msgId, src, "double", false, 0U, &dims);
  ret = *(real_T *)mxGetData(src);
  emlrtDestroyArray(&src);
  return ret;
}

void NormalErrorCoef2_api(const mxArray * const prhs[7], const mxArray *plhs[1])
{
  real_T (*Rtot)[12];
  real_T (*KdMat)[60];
  real_T (*mfiAdjMean)[192];
  real_T (*tnpbsa)[2];
  real_T (*meanPerCond)[48];
  real_T (*biCoefMat)[900];
  real_T whichR;
  emlrtStack st = { NULL, NULL, NULL };

  st.tls = emlrtRootTLSGlobal;

  /* Marshall function inputs */
  Rtot = emlrt_marshallIn(&st, emlrtAlias(prhs[0]), "Rtot");
  KdMat = c_emlrt_marshallIn(&st, emlrtAlias(prhs[1]), "KdMat");
  mfiAdjMean = e_emlrt_marshallIn(&st, emlrtAlias(prhs[2]), "mfiAdjMean");
  tnpbsa = g_emlrt_marshallIn(&st, emlrtAlias(prhs[3]), "tnpbsa");
  meanPerCond = i_emlrt_marshallIn(&st, emlrtAlias(prhs[4]), "meanPerCond");
  biCoefMat = k_emlrt_marshallIn(&st, emlrtAlias(prhs[5]), "biCoefMat");
  whichR = m_emlrt_marshallIn(&st, emlrtAliasP(prhs[6]), "whichR");

  /* Invoke the target function */
  whichR = NormalErrorCoef2(&st, *Rtot, *KdMat, *mfiAdjMean, *tnpbsa,
    *meanPerCond, *biCoefMat, whichR);

  /* Marshall function outputs */
  plhs[0] = emlrt_marshallOut(whichR);
}

/* End of code generation (_coder_NormalErrorCoef2_api.c) */
