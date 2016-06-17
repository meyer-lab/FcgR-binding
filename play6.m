fun = @(x) x^3;
test = fminunc('autodiff',2,[],fun)