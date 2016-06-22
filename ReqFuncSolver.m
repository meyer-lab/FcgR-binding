function x = ReqFuncSolver(R, kdi, Li, vi, kx)
    %%%This function returns the point at which function fun equals zero
    %%%using the bisection algorithm. The closest a and b will converge to
    %%%in the algorithm is a distance 1e-12 apart.
    
    a = -5;
    b = 5;
    error = 10;
    
    %Commence algorithm
    while 1
        c = (a+b)/2;
        if abs(fun(c, R, kdi, Li, vi, kx)) < error
            x = c;
            return;
        end
        if fun(c, R, kdi, Li, vi, kx)*fun(b, R, kdi, Li, vi, kx) >= 0
            b = c;
        else
            a = c;
        end
        %Returns a NaN if a and b come with 1e-12 of each other before
        %convergence
        if b-a < 1e-12
            x = 6;
            return
        end
    end
end
%-------------------------------------------------------------------------
function diff = fun(x, R, kdi, Li, vi, kx)
    diff = R - 10^x*(1+vi*Li/kdi*(1+kx*10^x)^(vi-1));
end