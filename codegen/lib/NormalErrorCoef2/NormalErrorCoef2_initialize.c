/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalErrorCoef2_initialize.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 15-Aug-2016 17:19:22
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef2.h"
#include "NormalErrorCoef2_initialize.h"
#include "NormalErrorCoef2_data.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void NormalErrorCoef2_initialize(void)
{
  rt_InitInfAndNaN(8U);
  omp_init_nest_lock(&emlrtNestLockGlobal);
}

/*
 * File trailer for NormalErrorCoef2_initialize.c
 *
 * [EOF]
 */
