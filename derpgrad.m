function grad = derpgrad(F,X0,epsilon)
    %only works for row vectors
    if size(X0,1) > 1
        error('Vector must be a column vector.')
    end
    grad = zeros(size(X0));
    for j = 1:length(grad)
        a = X0(1:j-1);
        b = X0(j+1:length(grad));
        grad(j) = derpderiv(@(x) F([a x b]),X0(j),epsilon);
    end
end