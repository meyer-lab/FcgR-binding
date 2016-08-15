/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * PROPRND_initialize.c
 *
 * Code generation for function 'PROPRND_initialize'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "PROPRND_initialize.h"
#include "_coder_PROPRND_mex.h"
#include "PROPRND_data.h"

/* Function Declarations */
static void PROPRND_once(void);

/* Function Definitions */
static void PROPRND_once(void)
{
  /* Allocate instance data */
  covrtAllocateInstanceData(&emlrtCoverageInstance);

  /* Initialize Coverage Information */
  covrtScriptInit(&emlrtCoverageInstance,
                  "C:\\Users\\mitadm\\Downloads\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\recepnum1-e341e5ae190230fa1e37b36ad6975b293cd98acc\\"
                  "PROPRND.m", 0, 2, 19, 1, 0, 0, 0, 2, 6, 0, 0);

  /* Initialize Function Information */
  covrtFcnInit(&emlrtCoverageInstance, 0, 0, "PROPRND", 0, -1, 1519);
  covrtFcnInit(&emlrtCoverageInstance, 0, 1, "twotailexprnd", 1596, -1, 1948);

  /* Initialize Basic Block Information */
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 2, 396, -1, 432);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 3, 454, -1, 468);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 1, 295, -1, 339);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 5, 608, -1, 645);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 8, 862, -1, 898);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 9, 920, -1, 934);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 7, 761, -1, 805);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 11, 1124, -1, 1146);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 13, 1230, -1, 1253);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 15, 1445, -1, 1485);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 16, 1499, -1, 1514);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 14, 1267, -1, 1388);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 12, 1160, -1, 1177);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 10, 985, -1, 1070);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 6, 659, -1, 673);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 4, 517, -1, 557);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 0, 167, -1, 233);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 18, 1925, -1, 1935);
  covrtBasicBlockInit(&emlrtCoverageInstance, 0, 17, 1853, -1, 1898);

  /* Initialize If Information */
  covrtIfInit(&emlrtCoverageInstance, 0, 0, 1904, 1916, -1, 1944);

  /* Initialize MCDC Information */
  /* Initialize For Information */
  covrtForInit(&emlrtCoverageInstance, 0, 0, 275, 287, 477);
  covrtForInit(&emlrtCoverageInstance, 0, 1, 741, 753, 943);

  /* Initialize While Information */
  covrtWhileInit(&emlrtCoverageInstance, 0, 0, 349, 384, 445);
  covrtWhileInit(&emlrtCoverageInstance, 0, 1, 563, 600, 654);
  covrtWhileInit(&emlrtCoverageInstance, 0, 2, 815, 850, 911);
  covrtWhileInit(&emlrtCoverageInstance, 0, 3, 1076, 1115, 1155);
  covrtWhileInit(&emlrtCoverageInstance, 0, 4, 1183, 1222, 1262);
  covrtWhileInit(&emlrtCoverageInstance, 0, 5, 1394, 1437, 1494);

  /* Initialize Switch Information */
  /* Start callback for coverage engine */
  covrtScriptStart(&emlrtCoverageInstance, 0U);
}

void PROPRND_initialize(void)
{
  emlrtStack st = { NULL, NULL, NULL };

  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtLicenseCheckR2012b(&st, "Statistics_Toolbox", 2);
  if (emlrtFirstTimeR2012b(emlrtRootTLSGlobal)) {
    PROPRND_once();
  }
}

/* End of code generation (PROPRND_initialize.c) */
