/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalError_initialize.c
 *
 * Code generation for function 'NormalError_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalError.h"
#include "NormalError_initialize.h"
#include "_coder_NormalError_mex.h"
#include "NormalError_data.h"

/* Function Declarations */
static void NormalError_once(void);

/* Function Definitions */
static void NormalError_once(void)
{
  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum2\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\NormalError.m",
                  0, 2, 7, 0, 0, 0, 0, 4, 0, 0, 0);

  /* Initialize Function Information */
  covrtFcnInit(&emlrtCoverageInstance, 0, 0, "NormalError", 0, -1, 842);
  covrtFcnInit(&emlrtCoverageInstance, 0, 1, "pseudoNormlike", 919, -1, 1204);

  /* Initialize Basic Block Information */
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 5, 797, -1, 837);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 4, 603, -1, 735);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 3, 355, -1, 553);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 2, 299, -1, 313);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 1, 202, -1, 265);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 0, 102, -1, 176);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 6, 1128, -1, 1199);

  /* Initialize If Information */
  /* Initialize MCDC Information */
  /* Initialize For Information */
  covrtForInit(&emlrtCoverageInstance, 0, 0, 182, 194, 792);
  covrtForInit(&emlrtCoverageInstance, 0, 1, 275, 287, 784);
  covrtForInit(&emlrtCoverageInstance, 0, 2, 327, 339, 772);
  covrtForInit(&emlrtCoverageInstance, 0, 3, 571, 583, 756);

  /* Initialize While Information */
  /* Initialize Switch Information */
  /* Start callback for coverage engine */
  covrtScriptStart(&emlrtCoverageInstance, 0U);

  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum2\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\StoneMod.m",
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

void NormalError_initialize(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtLicenseCheckR2012b(&st, "Statistics_Toolbox", 2);
  if (emlrtFirstTimeR2012b(emlrtRootTLSGlobal)) {
    NormalError_once();
  }
}

/* End of code generation (NormalError_initialize.c) */
