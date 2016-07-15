/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalErrorId_initialize.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 15-Jul-2016 12:51:37
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalErrorId.h"
#include "NormalErrorId_initialize.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void NormalErrorId_initialize(void)
{
  rt_InitInfAndNaN(8U);
}

/*
 * File trailer for NormalErrorId_initialize.c
 *
 * [EOF]
 */
