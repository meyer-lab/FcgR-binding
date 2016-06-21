function x = ReqFuncSolver(R, kdi, Li, vi, kx, a, b, error)
    %%%This function uses the bisection algorithm so solve the equation
    %%%represented by the anonymous function ReqFunc in Error.
    
    %Check that the first point on the interval is less than the second, 
    %that fun(a)*fun(b) is negative, and that error is positive. If not, 
    %return an imaginary number.
    if a >= b || (R - a*(1+vi*Li/kdi*(1+kx*a)^(vi-1)))*(R - b*(1+vi*Li/kdi*(1+kx*b)^(vi-1))) >= 0 ...
            || error <= 0
        x = i;
        return
    end
    
    %Commence algorithm
    condition = 0;
    while condition == 0
        c = (a+b)/2;
        if abs(R - c*(1+vi*Li/kdi*(1+kx*c)^(vi-1))) < error
            condition = 1;
            x = c;
        end
        if (R - c*(1+vi*Li/kdi*(1+kx*c)^(vi-1)))*(R - b*(1+vi*Li/kdi*(1+kx*b)^(vi-1))) >= 0
            b = c;
        else
            a = c;
        end
        %Returns a NaN if a and b come with 1e-12 of each other before
        %convergence
        if b-a < 1e-12
            x = i;
            return
        end
    end
end