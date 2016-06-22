/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * scalexpAlloc.c
 *
 * Code generation for function 'scalexpAlloc'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PDF.h"
#include "scalexpAlloc.h"

/* Function Definitions */
boolean_T b_dimagree(const emxArray_real_T *z, const emxArray_real_T *varargin_2)
{
  boolean_T p;
  boolean_T b_p;
  int32_T k;
  boolean_T exitg1;
  p = true;
  b_p = true;
  k = 0;
  exitg1 = false;
  while ((!exitg1) && (k + 1 < 3)) {
    if (z->size[k] != varargin_2->size[k]) {
      b_p = false;
      exitg1 = true;
    } else {
      k++;
    }
  }

  if (b_p) {
  } else {
    p = false;
  }

  return p;
}

boolean_T dimagree(const emxArray_real_T *z, const emxArray_real_T *varargin_2)
{
  boolean_T p;
  boolean_T b_p;
  int32_T k;
  boolean_T exitg1;
  int32_T i0;
  int32_T i1;
  p = true;
  b_p = true;
  k = 1;
  exitg1 = false;
  while ((!exitg1) && (k < 3)) {
    if (k <= 1) {
      i0 = z->size[0];
    } else {
      i0 = 1;
    }

    if (k <= 1) {
      i1 = varargin_2->size[0];
    } else {
      i1 = 1;
    }

    if (i0 != i1) {
      b_p = false;
      exitg1 = true;
    } else {
      k++;
    }
  }

  if (b_p) {
  } else {
    p = false;
  }

  return p;
}

/* End of code generation (scalexpAlloc.c) */
