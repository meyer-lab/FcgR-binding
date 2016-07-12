function [x, fval] = play7(meanPerCond,stdPerCond)
    [x, fval] = fmincon(@(x) Err(x(1), stdPerCond, meanPerCond, x(2)),[1;1],[],[]);
end
%--------------------------------------------------------------------------
function negJ = Err(a, stdPerCond, meanPerCond, sigma)
    J = 0;
    for j = 1:24
        for k = 1:2
            J = J + pseudoNormlike(stdPerCond(j,k),a*meanPerCond(j,k),sigma);
        end
    end
    negJ = -J;
end
%--------------------------------------------------------------------------
function logprob = pseudoNormlike(x,mu,sigma)
    %To replace normlike in the function PDF; while normlike returns
    %negated log probabilities, this function returns log probabilities as
    %they are.
    z = (x - mu) / sigma;
    logprob = -.5 * z^2 - log(sqrt(2.*pi).*sigma);
end