/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef2_initialize.c
 *
 * Code generation for function 'NormalErrorCoef2_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef2.h"
#include "NormalErrorCoef2_initialize.h"
#include "_coder_NormalErrorCoef2_mex.h"
#include "NormalErrorCoef2_data.h"

/* Function Declarations */
static void NormalErrorCoef2_once(void);

/* Function Definitions */
static void NormalErrorCoef2_once(void)
{
  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\admin\\Documents\\GitHub\\recepnum1\\NormalErrorCoef2.m",
                  0, 2, 6, 0, 0, 0, 0, 3, 0, 0, 0);

  /* Initialize Function Information */
  covrtFcnInit(&emlrtCoverageInstance, 0, 0, "NormalErrorCoef2", 0, -1, 855);
  covrtFcnInit(&emlrtCoverageInstance, 0, 1, "pseudoNormlike", 932, -1, 1217);

  /* Initialize Basic Block Information */
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 4, 810, -1, 850);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 3, 639, -1, 768);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 2, 331, -1, 597);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 1, 234, -1, 297);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 0, 111, -1, 208);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 5, 1141, -1, 1212);

  /* Initialize If Information */
  /* Initialize MCDC Information */
  /* Initialize For Information */
  covrtForInit(&emlrtCoverageInstance, 0, 0, 214, 226, 805);
  covrtForInit(&emlrtCoverageInstance, 0, 1, 307, 319, 797);
  covrtForInit(&emlrtCoverageInstance, 0, 2, 611, 623, 785);

  /* Initialize While Information */
  /* Initialize Switch Information */
  /* Start callback for coverage engine */
  covrtScriptStart(&emlrtCoverageInstance, 0U);

  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\admin\\Documents\\GitHub\\recepnum1\\StoneMod.m",
                  1, 3, 8, 2, 0, 0, 0, 0, 1, 0, 0);

  /* Initialize Function Information */
  covrtFcnInit(&emlrtCoverageInstance, 1, 0, "StoneMod", 0, -1, 820);
  covrtFcnInit(&emlrtCoverageInstance, 1, 1, "ReqFuncSolver", 897, -1, 1810);
  covrtFcnInit(&emlrtCoverageInstance, 1, 2, "fun", 1887, -1, 1994);

  /* Initialize Basic Block Information */
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 0, 549, -1, 815);
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 2, 1370, -1, 1394);
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 6, 1780, -1, 1785);
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 5, 1723, -1, 1753);
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 4, 1620, -1, 1674);
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 3, 1529, -1, 1537);
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 1, 1152, -1, 1290);
  covrtBasicBlockInit(&emlrtCoverageInstance, 1, 7, 1934, -1, 1989);

  /* Initialize If Information */
  covrtIfInit(&emlrtCoverageInstance, 1, 0, 1345, 1361, 1567, 1806);
  covrtIfInit(&emlrtCoverageInstance, 1, 1, 1693, 1710, 1763, 1798);

  /* Initialize MCDC Information */
  /* Initialize For Information */
  /* Initialize While Information */
  covrtWhileInit(&emlrtCoverageInstance, 1, 0, 1567, 1611, 1806);

  /* Initialize Switch Information */
  /* Start callback for coverage engine */
  covrtScriptStart(&emlrtCoverageInstance, 1U);
}

void NormalErrorCoef2_initialize(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtLicenseCheckR2012b(&st, "Statistics_Toolbox", 2);
  if (emlrtFirstTimeR2012b(emlrtRootTLSGlobal)) {
    NormalErrorCoef2_once();
  }
}

/* End of code generation (NormalErrorCoef2_initialize.c) */
