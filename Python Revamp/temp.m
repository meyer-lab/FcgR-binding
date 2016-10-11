function c = ReqFuncSolver(R, kdi, Li, vi, kx)
    %%%This function returns the point at which function fun equals zero
    %%using the bisection algorithm. The closest a and b will converge to
    %%in the algorithm is a distance 1e-12 apart.
    
    viLikdi = vi*Li/kdi;
    
    a = -20;
    b = log10(R);
    disp(a)
    disp(b)
    disp(char(10))
    
    bVal = fun(b, R, vi, kx, viLikdi);
    cVal = fun(a, R, vi, kx, viLikdi);
    disp([bVal;cVal])
    
    % Is there no root within the interval?
    if bVal*cVal > 0
        c = 1000;
        return;
    end
    
    %In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin
    %with; only implemented for MATLAB Coder
    c = 1000;
    %Commence algorithm
    while ((b - a > 1e-4) && (abs(cVal) > 1e-4))
        c = (a+b)/2;
%         disp([bVal;cVal])
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