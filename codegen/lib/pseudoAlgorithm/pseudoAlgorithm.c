/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: pseudoAlgorithm.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "PDF.h"
#include "rand.h"
#include "randn.h"
#include "PROPRND.h"
#include "pseudoAlgorithm_emxutil.h"
#include "randi.h"

/* Function Definitions */

/*
 * Arguments    : double nsamples
 *                double goodsize
 *                double mehsize
 *                const double kdBruhns[24]
 *                const double tnpbsa[2]
 *                const double mfiAdjMean[192]
 *                const double best[7]
 *                const double meanPerCond[48]
 *                const double stdPerCond[48]
 *                const double biCoefMat[676]
 *                emxArray_real_T *good
 *                emxArray_real_T *goodfit
 *                emxArray_real_T *meh
 * Return Type  : void
 */
void pseudoAlgorithm(double nsamples, double goodsize, double mehsize, const
                     double kdBruhns[24], const double tnpbsa[2], const double
                     mfiAdjMean[192], const double best[7], const double
                     meanPerCond[48], const double stdPerCond[48], const double
                     biCoefMat[676], emxArray_real_T *good, emxArray_real_T
                     *goodfit, emxArray_real_T *meh)
{
  int i0;
  int k;
  emxArray_real_T *r0;
  emxArray_real_T *r1;
  emxArray_real_T *b;
  int unnamed_idx_0;
  int b_unnamed_idx_0;
  int i1;
  int j;
  double b_good[11];
  int b_k;
  double temp[11];
  double r[9];
  boolean_T x[9];
  double y;
  boolean_T guard1 = false;
  double b_r;
  int l;
  double tempfit;
  double goodtemp[11];
  (void)best;
  i0 = good->size[0] * good->size[1] * good->size[2];
  good->size[0] = (int)goodsize;
  good->size[1] = 11;
  good->size[2] = (int)(nsamples * (goodsize + mehsize) + 1.0);
  emxEnsureCapacity((emxArray__common *)good, i0, (int)sizeof(double));
  k = (int)goodsize * 11 * (int)(nsamples * (goodsize + mehsize) + 1.0);
  for (i0 = 0; i0 < k; i0++) {
    good->data[i0] = 0.0;
  }

  i0 = meh->size[0] * meh->size[1] * meh->size[2];
  meh->size[0] = (int)mehsize;
  meh->size[1] = 11;
  meh->size[2] = (int)(nsamples + 1.0);
  emxEnsureCapacity((emxArray__common *)meh, i0, (int)sizeof(double));
  k = (int)mehsize * 11 * (int)(nsamples + 1.0);
  for (i0 = 0; i0 < k; i0++) {
    meh->data[i0] = 0.0;
  }

  emxInit_real_T(&r0, 1);
  emxInit_real_T(&r1, 1);
  emxInit_real_T1(&b, 2);
  randi(goodsize, r0);
  b_randi(goodsize, r1);
  b_rand(goodsize, b);
  unnamed_idx_0 = r0->size[0];
  b_unnamed_idx_0 = r1->size[0];
  for (i0 = 0; i0 < 9; i0++) {
    k = b->size[0];
    for (i1 = 0; i1 < k; i1++) {
      good->data[i1 + good->size[0] * i0] = 25.0 * b->data[i1 + b->size[0] * i0]
        - 20.0;
    }
  }

  for (i0 = 0; i0 < unnamed_idx_0; i0++) {
    good->data[i0 + good->size[0] * 9] = r0->data[i0];
  }

  for (i0 = 0; i0 < b_unnamed_idx_0; i0++) {
    good->data[i0 + good->size[0] * 10] = r1->data[i0];
  }

  randi(mehsize, r0);
  b_randi(mehsize, r1);
  b_rand(mehsize, b);
  unnamed_idx_0 = r0->size[0];
  b_unnamed_idx_0 = r1->size[0];
  for (i0 = 0; i0 < 9; i0++) {
    k = b->size[0];
    for (i1 = 0; i1 < k; i1++) {
      meh->data[i1 + meh->size[0] * i0] = 25.0 * b->data[i1 + b->size[0] * i0] -
        20.0;
    }
  }

  emxFree_real_T(&b);
  for (i0 = 0; i0 < unnamed_idx_0; i0++) {
    meh->data[i0 + meh->size[0] * 9] = r0->data[i0];
  }

  emxFree_real_T(&r0);
  for (i0 = 0; i0 < b_unnamed_idx_0; i0++) {
    meh->data[i0 + meh->size[0] * 10] = r1->data[i0];
  }

  emxFree_real_T(&r1);
  i0 = goodfit->size[0] * goodfit->size[1];
  goodfit->size[0] = (int)goodsize;
  goodfit->size[1] = (int)(nsamples * (goodsize + mehsize) + 1.0);
  emxEnsureCapacity((emxArray__common *)goodfit, i0, (int)sizeof(double));
  k = (int)goodsize * (int)(nsamples * (goodsize + mehsize) + 1.0);
  for (i0 = 0; i0 < k; i0++) {
    goodfit->data[i0] = 0.0;
  }

  for (j = 0; j < (int)goodsize; j++) {
    for (i0 = 0; i0 < 11; i0++) {
      b_good[i0] = good->data[j + good->size[0] * i0];
    }

    goodfit->data[j] = PDF(b_good, kdBruhns, mfiAdjMean, biCoefMat, tnpbsa,
      meanPerCond, stdPerCond);
  }

  for (j = 0; j < (int)nsamples; j++) {
    for (b_k = 0; b_k < (int)mehsize; b_k++) {
      memset(&temp[0], 0, 11U * sizeof(double));
      randn(r);
      for (i0 = 0; i0 < 9; i0++) {
        r[i0] *= 0.1;
      }

      for (i0 = 0; i0 < 9; i0++) {
        temp[i0] = meh->data[(b_k + meh->size[0] * i0) + meh->size[0] *
          meh->size[1] * j] + r[i0];
      }

      for (i0 = 0; i0 < 9; i0++) {
        x[i0] = (temp[i0] <= -20.0);
      }

      y = x[0];
      for (k = 0; k < 8; k++) {
        y += (double)x[k + 1];
      }

      guard1 = false;
      if (y != 0.0) {
        guard1 = true;
      } else {
        for (i0 = 0; i0 < 9; i0++) {
          x[i0] = (temp[i0] >= 5.0);
        }

        y = x[0];
        for (k = 0; k < 8; k++) {
          y += (double)x[k + 1];
        }

        if (y != 0.0) {
          guard1 = true;
        } else {
          while ((temp[9] < 1.0) || (4.0 < temp[9])) {
            y = f_rand();
            temp[9] = (meh->data[(b_k + meh->size[0] * 9) + meh->size[0] *
                       meh->size[1] * j] + (1.0 + floor(y * 3.0))) - 2.0;
          }

          while ((temp[10] < 1.0) || (26.0 < temp[10])) {
            y = f_rand();
            temp[10] = (meh->data[(b_k + meh->size[0] * 10) + meh->size[0] *
                        meh->size[1] * j] + (1.0 + floor(y * 3.0))) - 2.0;
          }
        }
      }

      if (guard1) {
        d_rand(r);
        y = e_rand();
        b_r = e_rand();
        for (i0 = 0; i0 < 9; i0++) {
          temp[i0] = 25.0 * r[i0] - 20.0;
        }

        temp[9] = 1.0 + floor(y * 4.0);
        temp[10] = 1.0 + floor(b_r * 26.0);
      }

      for (i0 = 0; i0 < 11; i0++) {
        meh->data[(b_k + meh->size[0] * i0) + meh->size[0] * meh->size[1] *
          ((int)((1.0 + (double)j) + 1.0) - 1)] = temp[i0];
      }
    }

    for (b_k = 0; b_k < (int)goodsize; b_k++) {
      for (l = 0; l < (int)mehsize; l++) {
        for (i0 = 0; i0 < 11; i0++) {
          b_good[i0] = meh->data[(l + meh->size[0] * i0) + meh->size[0] *
            meh->size[1] * j];
        }

        PROPRND(b_good, temp);
        tempfit = PDF(temp, kdBruhns, mfiAdjMean, biCoefMat, tnpbsa, meanPerCond,
                      stdPerCond);
        i0 = (int)(((1.0 + (double)j) - 1.0) * (goodsize + mehsize) + (1.0 +
                    (double)l));
        for (i1 = 0; i1 < 11; i1++) {
          goodtemp[i1] = good->data[(b_k + good->size[0] * i1) + good->size[0] *
            good->size[1] * (i0 - 1)];
        }

        if (tempfit - goodfit->data[b_k + goodfit->size[0] * ((int)(((1.0 +
                (double)j) - 1.0) * (goodsize + mehsize) + (1.0 + (double)l)) -
             1)] < 0.0) {
          if (f_rand() < exp(tempfit - goodfit->data[b_k + goodfit->size[0] *
                             ((int)(((1.0 + (double)j) - 1.0) * (goodsize +
                  mehsize) + (1.0 + (double)l)) - 1)])) {
            i0 = (int)((1.0 + ((1.0 + (double)j) - 1.0) * (goodsize + mehsize))
                       + (1.0 + (double)l));
            for (i1 = 0; i1 < 11; i1++) {
              good->data[(b_k + good->size[0] * i1) + good->size[0] * good->
                size[1] * (i0 - 1)] = temp[i1];
            }

            goodfit->data[b_k + goodfit->size[0] * ((int)((1.0 + ((1.0 + (double)
              j) - 1.0) * (goodsize + mehsize)) + (1.0 + (double)l)) - 1)] =
              tempfit;
          } else {
            i0 = (int)((1.0 + ((1.0 + (double)j) - 1.0) * (goodsize + mehsize))
                       + (1.0 + (double)l));
            for (i1 = 0; i1 < 11; i1++) {
              good->data[(b_k + good->size[0] * i1) + good->size[0] * good->
                size[1] * (i0 - 1)] = goodtemp[i1];
            }

            goodfit->data[b_k + goodfit->size[0] * ((int)((1.0 + ((1.0 + (double)
              j) - 1.0) * (goodsize + mehsize)) + (1.0 + (double)l)) - 1)] =
              goodfit->data[b_k + goodfit->size[0] * ((int)(((1.0 + (double)j) -
              1.0) * (goodsize + mehsize) + (1.0 + (double)l)) - 1)];
          }
        } else {
          i0 = (int)((1.0 + ((1.0 + (double)j) - 1.0) * (goodsize + mehsize)) +
                     (1.0 + (double)l));
          for (i1 = 0; i1 < 11; i1++) {
            good->data[(b_k + good->size[0] * i1) + good->size[0] * good->size[1]
              * (i0 - 1)] = temp[i1];
          }

          goodfit->data[b_k + goodfit->size[0] * ((int)((1.0 + ((1.0 + (double)j)
            - 1.0) * (goodsize + mehsize)) + (1.0 + (double)l)) - 1)] = tempfit;
        }
      }

      for (l = 0; l < (int)goodsize; l++) {
        i0 = (int)((((1.0 + (double)j) - 1.0) * (goodsize + mehsize) + mehsize)
                   + (1.0 + (double)l));
        for (i1 = 0; i1 < 11; i1++) {
          b_good[i1] = good->data[(l + good->size[0] * i1) + good->size[0] *
            good->size[1] * (i0 - 1)];
        }

        PROPRND(b_good, temp);
        tempfit = PDF(temp, kdBruhns, mfiAdjMean, biCoefMat, tnpbsa, meanPerCond,
                      stdPerCond);
        i0 = (int)((((1.0 + (double)j) - 1.0) * (goodsize + mehsize) + mehsize)
                   + (1.0 + (double)l));
        for (i1 = 0; i1 < 11; i1++) {
          goodtemp[i1] = good->data[(b_k + good->size[0] * i1) + good->size[0] *
            good->size[1] * (i0 - 1)];
        }

        if (tempfit - goodfit->data[b_k + goodfit->size[0] * ((int)((((1.0 +
                 (double)j) - 1.0) * (goodsize + mehsize) + mehsize) + (1.0 +
               (double)l)) - 1)] < 0.0) {
          if (f_rand() < exp(tempfit - goodfit->data[b_k + goodfit->size[0] *
                             ((int)((((1.0 + (double)j) - 1.0) * (goodsize +
                   mehsize) + mehsize) + (1.0 + (double)l)) - 1)])) {
            i0 = (int)(((1.0 + ((1.0 + (double)j) - 1.0) * (goodsize + mehsize))
                        + mehsize) + (1.0 + (double)l));
            for (i1 = 0; i1 < 11; i1++) {
              good->data[(b_k + good->size[0] * i1) + good->size[0] * good->
                size[1] * (i0 - 1)] = temp[i1];
            }

            goodfit->data[b_k + goodfit->size[0] * ((int)(((1.0 + ((1.0 +
              (double)j) - 1.0) * (goodsize + mehsize)) + mehsize) + (1.0 +
              (double)l)) - 1)] = tempfit;
          } else {
            i0 = (int)(((1.0 + ((1.0 + (double)j) - 1.0) * (goodsize + mehsize))
                        + mehsize) + (1.0 + (double)l));
            for (i1 = 0; i1 < 11; i1++) {
              good->data[(b_k + good->size[0] * i1) + good->size[0] * good->
                size[1] * (i0 - 1)] = goodtemp[i1];
            }

            goodfit->data[b_k + goodfit->size[0] * ((int)(((1.0 + ((1.0 +
              (double)j) - 1.0) * (goodsize + mehsize)) + mehsize) + (1.0 +
              (double)l)) - 1)] = goodfit->data[b_k + goodfit->size[0] * ((int)
              ((((1.0 + (double)j) - 1.0) * (goodsize + mehsize) + mehsize) +
               (1.0 + (double)l)) - 1)];
          }
        } else {
          i0 = (int)(((1.0 + ((1.0 + (double)j) - 1.0) * (goodsize + mehsize)) +
                      mehsize) + (1.0 + (double)l));
          for (i1 = 0; i1 < 11; i1++) {
            good->data[(b_k + good->size[0] * i1) + good->size[0] * good->size[1]
              * (i0 - 1)] = temp[i1];
          }

          goodfit->data[b_k + goodfit->size[0] * ((int)(((1.0 + ((1.0 + (double)
            j) - 1.0) * (goodsize + mehsize)) + mehsize) + (1.0 + (double)l)) -
            1)] = tempfit;
        }
      }
    }
  }
}

/*
 * File trailer for pseudoAlgorithm.c
 *
 * [EOF]
 */
