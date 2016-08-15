/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: eml_rand_mcg16807_stateful.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 27-Jul-2016 10:12:22
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "eml_rand_mcg16807_stateful.h"
#include "PROPRND_data.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void eml_rand_mcg16807_stateful_init(void)
{
  state = 1144108930U;
}

/*
 * File trailer for eml_rand_mcg16807_stateful.c
 *
 * [EOF]
 */
