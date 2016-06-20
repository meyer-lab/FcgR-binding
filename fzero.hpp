/*
 *  fzero.hpp
 *  fzero
 *
 *  Created by Aaron Meyer on 6/18/16.
 *  Copyright © 2016 Aaron Meyer. All rights reserved.
 *
 */

#ifndef fzero_
#define fzero_

#include <vector>

/* The classes below are exported */
#pragma GCC visibility push(default)

extern "C" void bisectMat(double vi, double Li, double *kdi, double kx, double *R, int N, double *output);

#pragma GCC visibility pop
#endif