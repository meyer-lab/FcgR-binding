function L = StoneSolver(Rtot,Kx,v,Kd,L0,biCoefMat)    
    %Using the information given, finds the sum L presented in Equation 7
    %in Stone. In this context, all inputs save biCoefMat are scalars.
    
    %Solve for Req, as described in Equation 2 in Stone
    Req = ReqFuncSolver(Rtot, Kd, L0, v, Kx);
    %Check for error output from ReqFuncSolver
    if Req == 1000
        L = -1;
        return
    end
    %Convert from logarithmic scale
    Req = 10^Req;
    
    L = sum(L0/Kd*(biCoefMat(1:v,v)'.*(Kx.^([1:v]-1))).*Req.^[1:v]);
end
%--------------------------------------------------------------------------
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
    
    %In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin
    %with; only implemented for MATLAB Coder
    c = 1000;
    %Commence algorithm
    while b - a > 1e-4 || abs(cVal) > 1e-4
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
%--------------------------------------------------------------------------
function diff = fun(x, R, kdi, Li, vi, kx)
    diff = R - 10^x*(1+vi*Li/kdi*(1+kx*10^x)^(vi-1));
end