/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: randi.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "randi.h"
#include "rand.h"

/* Function Definitions */

/*
 * Arguments    : double varargin_1
 *                emxArray_real_T *r
 * Return Type  : void
 */
void b_randi(double varargin_1, emxArray_real_T *r)
{
  int i5;
  int k;
  c_rand(varargin_1, r);
  i5 = r->size[0];
  for (k = 0; k < i5; k++) {
    r->data[k] = 1.0 + floor(r->data[k] * 26.0);
  }
}

/*
 * Arguments    : double varargin_1
 *                emxArray_real_T *r
 * Return Type  : void
 */
void randi(double varargin_1, emxArray_real_T *r)
{
  int i3;
  int k;
  c_rand(varargin_1, r);
  i3 = r->size[0];
  for (k = 0; k < i3; k++) {
    r->data[k] = 1.0 + floor(r->data[k] * 4.0);
  }
}

/*
 * File trailer for randi.c
 *
 * [EOF]
 */
