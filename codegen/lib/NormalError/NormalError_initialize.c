/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalError_initialize.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 15-Jul-2016 09:48:12
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalError.h"
#include "NormalError_initialize.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void NormalError_initialize(void)
{
  rt_InitInfAndNaN(8U);
}

/*
 * File trailer for NormalError_initialize.c
 *
 * [EOF]
 */
