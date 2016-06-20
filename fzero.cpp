/*
 *  fzero.cpp
 *  fzero
 *
 *  Created by Aaron Meyer on 6/18/16.
 *  Copyright © 2016 Aaron Meyer. All rights reserved.
 *
 */

#include <iostream>
#include <cmath>
#include <vector>
#include "fzero.hpp"

using namespace std;

constexpr double e = 1E-4;

static double bisection(const double vi, const double Li, const double kdi, const double kx, const double R) {
    double a = -20;
    double b = 20;
    int counter = 0;
    double root = 0.0;
    double froot;

    auto f = [vi, Li, kdi, kx, R](double Reqi) {
        Reqi = pow(10, Reqi);

        return R - Reqi*(1+vi*Li/kdi*pow(1+kx*Reqi, vi-1));
    };

    double fa = f(a);

    if(fa * f(b) > 0)
        return -40;

    do {
        root = (a + b)/2;
        froot = f(root);

        if(fa * froot < 0) {
            b = root;
        } else {
            a = root;
            fa = froot;
        }

        counter++;
    } while (fabs(a - b) > e);

    return root;
}

void bisectMat(double vi, double Li, double *kdi, double kx, double *R, int N, double *output) {
    for (size_t ii = 0; ii < (size_t) N; ii++) {
        output[ii] = bisection(vi, Li, kdi[ii], kx, R[ii]);
    }
}