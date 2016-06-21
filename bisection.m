function [x] = bisection(fun,a,b,error)
    %%%This function returns the point at which function fun equals zero
    %%%using the bisection algorithm. The closest a and b will converge to
    %%%in the algorithm is a distance 1e-12 apart.
    
    %Check that the first point on the interval is less than the second, 
    %that fun(a)*fun(b) is negative, and that error is positive. If not, 
    %return an imaginary number.
    if a >= b || fun(a)*fun(b) >= 0 || error <= 0
        x = i;
        return
    end
    
    %Commence algorithm
    condition = 0;
    while condition == 0
        c = (a+b)/2;
        if abs(fun(c)) < error
            condition = 1;
            x = c;
        end
        if fun(c)*fun(b) >= 0
            b = c;
        else
            a = c;
        end
        %Returns a NaN if a and b come with 1e-12 of each other before
        %convergence
        if b-a < 1e-12
            x = NaN;
            return
        end
    end
end