/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: rand.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "rand.h"
#include "pseudoAlgorithm_emxutil.h"
#include "pseudoAlgorithm_data.h"

/* Function Definitions */

/*
 * Arguments    : double varargin_1
 *                emxArray_real_T *r
 * Return Type  : void
 */
void b_rand(double varargin_1, emxArray_real_T *r)
{
  int i2;
  int k;
  double d0;
  i2 = r->size[0] * r->size[1];
  r->size[0] = (int)varargin_1;
  r->size[1] = 9;
  emxEnsureCapacity((emxArray__common *)r, i2, (int)sizeof(double));
  i2 = r->size[0] * 9;
  for (k = 0; k < i2; k++) {
    d0 = genrandu(state);
    r->data[k] = d0;
  }
}

/*
 * Arguments    : double varargin_1
 *                emxArray_real_T *r
 * Return Type  : void
 */
void c_rand(double varargin_1, emxArray_real_T *r)
{
  int i4;
  int k;
  double d1;
  i4 = r->size[0];
  r->size[0] = (int)varargin_1;
  emxEnsureCapacity((emxArray__common *)r, i4, (int)sizeof(double));
  i4 = r->size[0];
  for (k = 0; k < i4; k++) {
    d1 = genrandu(state);
    r->data[k] = d1;
  }
}

/*
 * Arguments    : double r[9]
 * Return Type  : void
 */
void d_rand(double r[9])
{
  int k;
  double d3;
  for (k = 0; k < 9; k++) {
    d3 = genrandu(state);
    r[k] = d3;
  }
}

/*
 * Arguments    : void
 * Return Type  : double
 */
double e_rand(void)
{
  return genrandu(state);
}

/*
 * Arguments    : void
 * Return Type  : double
 */
double f_rand(void)
{
  return genrandu(state);
}

/*
 * Arguments    : unsigned int mt[625]
 *                unsigned int u[2]
 * Return Type  : void
 */
void genrand_uint32_vector(unsigned int mt[625], unsigned int u[2])
{
  int j;
  unsigned int mti;
  int kk;
  unsigned int y;
  unsigned int b_y;
  unsigned int c_y;
  unsigned int d_y;
  for (j = 0; j < 2; j++) {
    u[j] = 0U;
    mti = mt[624] + 1U;
    if (mti >= 625U) {
      for (kk = 0; kk < 227; kk++) {
        y = (mt[kk] & 2147483648U) | (mt[1 + kk] & 2147483647U);
        if ((int)(y & 1U) == 0) {
          b_y = y >> 1U;
        } else {
          b_y = y >> 1U ^ 2567483615U;
        }

        mt[kk] = mt[397 + kk] ^ b_y;
      }

      for (kk = 0; kk < 396; kk++) {
        y = (mt[kk + 227] & 2147483648U) | (mt[228 + kk] & 2147483647U);
        if ((int)(y & 1U) == 0) {
          c_y = y >> 1U;
        } else {
          c_y = y >> 1U ^ 2567483615U;
        }

        mt[kk + 227] = mt[kk] ^ c_y;
      }

      y = (mt[623] & 2147483648U) | (mt[0] & 2147483647U);
      if ((int)(y & 1U) == 0) {
        d_y = y >> 1U;
      } else {
        d_y = y >> 1U ^ 2567483615U;
      }

      mt[623] = mt[396] ^ d_y;
      mti = 1U;
    }

    y = mt[(int)mti - 1];
    mt[624] = mti;
    y ^= y >> 11U;
    y ^= y << 7U & 2636928640U;
    y ^= y << 15U & 4022730752U;
    y ^= y >> 18U;
    u[j] = y;
  }
}

/*
 * Arguments    : unsigned int mt[625]
 * Return Type  : double
 */
double genrandu(unsigned int mt[625])
{
  double r;
  int exitg1;
  unsigned int u[2];
  boolean_T isvalid;
  int k;
  boolean_T exitg2;
  unsigned int b_r;

  /* ========================= COPYRIGHT NOTICE ============================ */
  /*  This is a uniform (0,1) pseudorandom number generator based on:        */
  /*                                                                         */
  /*  A C-program for MT19937, with initialization improved 2002/1/26.       */
  /*  Coded by Takuji Nishimura and Makoto Matsumoto.                        */
  /*                                                                         */
  /*  Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura,      */
  /*  All rights reserved.                                                   */
  /*                                                                         */
  /*  Redistribution and use in source and binary forms, with or without     */
  /*  modification, are permitted provided that the following conditions     */
  /*  are met:                                                               */
  /*                                                                         */
  /*    1. Redistributions of source code must retain the above copyright    */
  /*       notice, this list of conditions and the following disclaimer.     */
  /*                                                                         */
  /*    2. Redistributions in binary form must reproduce the above copyright */
  /*       notice, this list of conditions and the following disclaimer      */
  /*       in the documentation and/or other materials provided with the     */
  /*       distribution.                                                     */
  /*                                                                         */
  /*    3. The names of its contributors may not be used to endorse or       */
  /*       promote products derived from this software without specific      */
  /*       prior written permission.                                         */
  /*                                                                         */
  /*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS    */
  /*  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT      */
  /*  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR  */
  /*  A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT  */
  /*  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  */
  /*  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT       */
  /*  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,  */
  /*  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY  */
  /*  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT    */
  /*  (INCLUDING  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE */
  /*  OF THIS  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  */
  /*                                                                         */
  /* =============================   END   ================================= */
  do {
    exitg1 = 0;
    genrand_uint32_vector(mt, u);
    r = 1.1102230246251565E-16 * ((double)(u[0] >> 5U) * 6.7108864E+7 + (double)
      (u[1] >> 6U));
    if (r == 0.0) {
      if ((mt[624] >= 1U) && (mt[624] < 625U)) {
        isvalid = true;
      } else {
        isvalid = false;
      }

      if (isvalid) {
        isvalid = false;
        k = 1;
        exitg2 = false;
        while ((!exitg2) && (k < 625)) {
          if (mt[k - 1] == 0U) {
            k++;
          } else {
            isvalid = true;
            exitg2 = true;
          }
        }
      }

      if (!isvalid) {
        b_r = 5489U;
        mt[0] = 5489U;
        for (k = 0; k < 623; k++) {
          b_r = (b_r ^ b_r >> 30U) * 1812433253U + (1 + k);
          mt[k + 1] = b_r;
        }

        mt[624] = 624U;
      }
    } else {
      exitg1 = 1;
    }
  } while (exitg1 == 0);

  return r;
}

/*
 * File trailer for rand.c
 *
 * [EOF]
 */
