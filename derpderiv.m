function deriv = derpderiv(F,x0,epsilon)
    if ~isscalar(x0)
        error('Input must be scalar.')
    end
    deriv = (F(x0+epsilon) - F(x0-epsilon))/(2*epsilon);
end