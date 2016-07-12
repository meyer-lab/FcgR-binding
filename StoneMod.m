function [L] = StoneMod(logR, Kd, v, logKx, L0)
    %Returns the number of mutlivalent ligand bound to a cell with 10^logR
    %receptors, granted each epitope of the ligand binds to the receptor
    %kind in question with dissociation constant Kd and cross-links with
    %other receptors with crosslinking constant Kx = 10^logKx. All
    %equations derived from Stone et al. (2001). Assumed that ligand is at
    %saturating concentration L0 = 7e-8 M, which is as it is (approximately)
    %for TNP-4-BSA in Lux et al. (2013).
    
    Kx = 10^logKx;
    R = 10^logR;
    
    %Vector of binomial coefficients
    biCoefVec = zeros(1,v);
    for j = 1:v
        biCoefVec(j) = nchoosek(v,j);
    end
    Req = 10^ReqFuncSolver(R,Kd,L0,v,Kx);
    
    %Calculate L, according to equations 1 and 7
    L = sum(biCoefVec.*(Kx.^([1:v]-1)).*(L0/Kd*(Req.^[1:v])));
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
    while b - a > 1e-4 || abs(cVal) > 1e-4
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