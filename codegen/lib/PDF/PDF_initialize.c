/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: PDF_initialize.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 07-Jul-2016 12:53:52
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "PDF_initialize.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void PDF_initialize(void)
{
  rt_InitInfAndNaN(8U);
}

/*
 * File trailer for PDF_initialize.c
 *
 * [EOF]
 */
