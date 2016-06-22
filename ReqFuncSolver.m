function c = ReqFuncSolver(R, kdi, Li, vi, kx)
    %%%This function returns the point at which function fun equals zero
    %%%using the bisection algorithm. The closest a and b will converge to
    %%%in the algorithm is a distance 1e-12 apart.
    
    a = -20;
    b = log10(R);
    
    bVal = fun(b, R, kdi, Li, vi, kx);
    cVal = fun(a, R, kdi, Li, vi, kx);
    
    % Is there no root within the interval?
    if bVal*cVal > 0
        c = 1000;
        return;
    end
    
    %Commence algorithm
    while b - a > 1e-4 || abs(cVal) > 1E-4
        c = (a+b)/2;
        cVal = fun(c, R, kdi, Li, vi, kx);
        
        if cVal*bVal >= 0
            b = c;
            bVal = cVal;
        else
            a = c;
        end
    end
end
%-------------------------------------------------------------------------
function diff = fun(x, R, kdi, Li, vi, kx)
    diff = R - 10^x*(1+vi*Li/kdi*(1+kx*10^x)^(vi-1));
end