function deriv = derpderiv(F,x0,epsilon)
    if ~isscalar(x0)
        error('Input must be scalar.')
    end
    deriv = (F(x+epsilon) - F(x-epsilon))/(2*epsilon);
end