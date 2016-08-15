/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * NormalError2_initialize.c
 *
 * Code generation for function 'NormalError2_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "NormalError2.h"
#include "NormalError2_initialize.h"
#include "_coder_NormalError2_mex.h"
#include "NormalError2_data.h"

/* Function Declarations */
static void NormalError2_once(void);

/* Function Definitions */
static void NormalError2_once(void)
{
  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\mitadm\\Documents\\GitHub\\recepnum2\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\NormalError2.m",
                  0, 2, 6, 0, 0, 0, 0, 3, 0, 0, 0);

  /* Initialize Function Information */
  covrtFcnInit(&emlrtCoverageInstance, 0, 0, "NormalError2", 0, -1, 786);
  covrtFcnInit(&emlrtCoverageInstance, 0, 1, "pseudoNormlike", 863, -1, 1148);

  /* Initialize Basic Block Information */
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 4, 741, -1, 781);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 3, 570, -1, 699);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 2, 327, -1, 528);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 1, 230, -1, 293);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 0, 111, -1, 204);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 5, 1072, -1, 1143);

  /* Initialize If Information */
  /* Initialize MCDC Information */
  /* Initialize For Information */
  covrtForInit(&emlrtCoverageInstance, 0, 0, 210, 222, 736);
  covrtForInit(&emlrtCoverageInstance, 0, 1, 303, 315, 728);
  covrtForInit(&emlrtCoverageInstance, 0, 2, 542, 554, 716);

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

void NormalError2_initialize(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtLicenseCheckR2012b(&st, "Statistics_Toolbox", 2);
  if (emlrtFirstTimeR2012b(emlrtRootTLSGlobal)) {
    NormalError2_once();
  }
}

/* End of code generation (NormalError2_initialize.c) */
