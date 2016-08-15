function [LigandMat] = LigandFinder(Rtot, Kd, mfiAdjMean, biCoefMat, tnpbsa)
    %Convert from log scale
    Rtot(1:7) = 10.^Rtot(1:7);
    Kx = Rtot(7);
    v = Rtot(10:11);
    
    %Get expected value of dimers formed (see Equation 6 from Stone and
    %read paragraph beneath for derivation
    LigandMat = zeros(6,8);
    for j = 1:6
        for k = 1:4
            LigandMat(j,k) = StoneSolver(Rtot(j),Kx,v(1),Kd(j,k), ...
                tnpbsa(1),biCoefMat);
            LigandMat(j,k+4) = StoneSolver(Rtot(j),Kx,v(2),Kd(j,k), ...
                tnpbsa(2),biCoefMat);
            LigandMat = LigandMat;
        end
    end
end
%--------------------------------------------------------------------------
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
    
    v = v;
    L = sum(L0/Kd*(biCoefMat(1:v,v)'.*(Kx.^([1:v]-1))).*Req.^[1:v]);
end
%--------------------------------------------------------------------------
function c = ReqFuncSolver(R, kdi, Li, vi, kx)
    %%%This function returns the point at which function fun equals zero
    %%%using the bisection algorithm. The closest a and b will converge to
    %%%in the algorithm is a distance 1e-12 apart.
    
    viLikdi = vi*Li/kdi;
    
    a = -20;
    b = log10(R);
    
    bVal = fun(b, R, vi, kx, viLikdi);
    cVal = fun(a, R, vi, kx, viLikdi);
    
    % Is there no root within the interval?
    if bVal*cVal > 0
        c = 1000;
        return;
    end
    
    %In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin
    %with; only implemented for MATLAB Coder
    c = 1000;
    %Commence algorithm
    while ~xor((b - a > 1e-4),(abs(cVal) > 1e-4)) || (b - a > 1e-4) &&...
            (abs(cVal) > 1e-4)
        c = (a+b)/2;
        cVal = fun(c, R, vi, kx, viLikdi);
        
        if cVal*bVal >= 0
            b = c;
            bVal = cVal;
        else
            a = c;
        end
    end
end
%--------------------------------------------------------------------------
function diff = fun(x, R, vi, kx, viLikdi)
    x = 10.^x;
    diff = R - x*(1+viLikdi*(1+kx*x)^(vi-1));
end