/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalErrorCoef_initialize.c
 *
 * Code generation for function 'NormalErrorCoef_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef.h"
#include "NormalErrorCoef_initialize.h"
#include "_coder_NormalErrorCoef_mex.h"
#include "NormalErrorCoef_data.h"

/* Function Declarations */
static void NormalErrorCoef_once(void);

/* Function Definitions */
static void NormalErrorCoef_once(void)
{
  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\NormalErrorCoef.m",
                  0, 2, 7, 0, 0, 0, 0, 4, 0, 0, 0);

  /* Initialize Function Information */
  covrtFcnInit(&emlrtCoverageInstance, 0, 0, "NormalErrorCoef", 0, -1, 919);
  covrtFcnInit(&emlrtCoverageInstance, 0, 1, "pseudoNormlike", 996, -1, 1281);

  /* Initialize Basic Block Information */
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 5, 874, -1, 914);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 4, 680, -1, 812);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 3, 359, -1, 630);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 2, 303, -1, 317);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 1, 206, -1, 269);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 0, 102, -1, 180);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 6, 1205, -1, 1276);

  /* Initialize If Information */
  /* Initialize MCDC Information */
  /* Initialize For Information */
  covrtForInit(&emlrtCoverageInstance, 0, 0, 186, 198, 869);
  covrtForInit(&emlrtCoverageInstance, 0, 1, 279, 291, 861);
  covrtForInit(&emlrtCoverageInstance, 0, 2, 331, 343, 849);
  covrtForInit(&emlrtCoverageInstance, 0, 3, 648, 660, 833);

  /* Initialize While Information */
  /* Initialize Switch Information */
  /* Start callback for coverage engine */
  covrtScriptStart(&emlrtCoverageInstance, 0U);

  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum1\\StoneMod.m",
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

void NormalErrorCoef_initialize(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtLicenseCheckR2012b(&st, "Statistics_Toolbox", 2);
  if (emlrtFirstTimeR2012b(emlrtRootTLSGlobal)) {
    NormalErrorCoef_once();
  }
}

/* End of code generation (NormalErrorCoef_initialize.c) */
