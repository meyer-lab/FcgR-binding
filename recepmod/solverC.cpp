#include <iostream>
#include <cmath>
#include <tuple>

using namespace std;

tuple<double, double, double> diffFAnon(double x, double R, double viLika, double kx, int vi) {
	// Mass balance for receptor species, to identify the amount of free receptor.
	double b = 1+kx*x;
	double aa = viLika*pow(b, vi-3);

	return {R-x*(1+aa*b*b), -(kx*vi*x+1)*aa*b - 1, -kx*(vi-1)*aa*(2+kx*vi*x)};
}

extern "C" double ReqFuncSolver(const double R, const double ka, const double Li, const int vi, const double kx) {
	/*
	The purpose of this function is to calculate the value of Req (from Eq 1
	from Stone) given parameters R, kai=Ka,Li=L, vi=v, and kx=Kx. It does this
	by performing the bisction algorithm on Eq 2 from Stone. The bisection
	algorithm is used to find log10(Req) which satisfies Eq 2 from Stone.
	*/
	double viLika = vi*Li*ka;

	if (get<0>(diffFAnon(0, R, viLika, kx, vi)) * get<0>(diffFAnon(R, R, viLika, kx, vi)) > 0)
		return NAN;

	// Implement Newton's method
	const size_t maxiter = 1000;
	const double tol = 1.48e-8;

	double p0 = R;
	double p = -10000;
	
	for (size_t iter = 0; iter < maxiter; iter++) {
		tuple<double, double, double> fder = diffFAnon(p0, R, viLika, kx, vi);
		if (get<1>(fder) == 0) {
			cout << "derivative was zero." << endl;
			return NAN;
		}

		if (get<2>(fder) == 0) {
			// Newton step
			p = p0 - get<0>(fder) / get<1>(fder);
		} else {
			// Parabolic Halley's method
			double discr = pow(get<1>(fder), 2) - 2 * get<0>(fder) * get<2>(fder);
			if (discr < 0) {
				p = p0 - get<1>(fder) / get<2>(fder);
			} else {
				p = p0 - 2*get<0>(fder) / (get<1>(fder) + copysign(sqrt(discr), get<1>(fder)));
			}
		}

		if (abs(p - p0) < tol) {
			return p;
		}
		p0 = p;
	}

	cout << "Failed to converge after " << maxiter << " iterations, value is " << p << endl;

	return NAN;
}
