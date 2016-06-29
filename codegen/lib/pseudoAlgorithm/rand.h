/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: rand.h
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

#ifndef __RAND_H__
#define __RAND_H__

/* Include Files */
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "rtwtypes.h"
#include "pseudoAlgorithm_types.h"

/* Function Declarations */
extern void b_rand(double varargin_1, emxArray_real_T *r);
extern void c_rand(double varargin_1, emxArray_real_T *r);
extern void d_rand(double r[9]);
extern double e_rand(void);
extern double f_rand(void);
extern void genrand_uint32_vector(unsigned int mt[625], unsigned int u[2]);
extern double genrandu(unsigned int mt[625]);

#endif

/*
 * File trailer for rand.h
 *
 * [EOF]
 */
