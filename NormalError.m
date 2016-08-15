function logSqrErr = NormalError(Rtot, KdMat, mfiAdjMean, tnpbsa,...
    meanPerCond, biCoefMat)

    sigCoef = 10^Rtot(12);
    logKx = Rtot(7);
    logSqrErrMat = zeros(24,8);
    for j = 1:2
        v = Rtot(9+j);
        c = 10^Rtot(7+j);
        L0 = tnpbsa(j);
        for k = 1:6
            logR = Rtot(k);
            for l = 1:4
                Kd = KdMat(k,l);
                MFI = c*StoneMod(logR,Kd,v,logKx,L0,biCoefMat);
                temp = mfiAdjMean(4*(k-1)+l,(4*(j-1)+1):(4*(j-1)+4));
                mean = meanPerCond(4*(k-1)+l,j);
                for m = 1:4
                    logSqrErrMat(4*(k-1)+l,4*(j-1)+m) = ...
                        pseudoNormlike(temp(m),MFI,...
                        sigCoef*mean);
                end
            end
        end
    end
    logSqrErr = nansum(nansum(logSqrErrMat));
end
%--------------------------------------------------------------------------
function logprob = pseudoNormlike(x,mu,sigma)
    %To replace normlike in the function PDF; while normlike returns
    %negated log probabilities, this function returns log probabilities as
    %they are.
    z = (x - mu) / sigma;
    logprob = -.5 * z^2 - log(sqrt(2.*pi).*sigma);
end