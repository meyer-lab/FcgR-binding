/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: eml_rand_shr3cong_stateful.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 27-Jul-2016 10:12:22
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "eml_rand_shr3cong_stateful.h"
#include "PROPRND_data.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void eml_rand_shr3cong_stateful_init(void)
{
  int i1;
  for (i1 = 0; i1 < 2; i1++) {
    b_state[i1] = 362436069U + 158852560U * i1;
  }
}

/*
 * File trailer for eml_rand_shr3cong_stateful.c
 *
 * [EOF]
 */
