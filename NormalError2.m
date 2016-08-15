function logSqrErr = NormalError2(Rtot, KdMat, mfiAdjMean, tnpbsa,...
    meanPerCond, biCoefMat, whichR)

    sigCoef = 10^Rtot(7);
    logKx = Rtot(2);
    logSqrErrMat = zeros(24,8);
    logR = Rtot(1);
    for j = 1:2
        v = Rtot(4+j);
        c = 10^Rtot(2+j);
        L0 = tnpbsa(j);
        for k = 1:4
            Kd = KdMat(whichR,k);
            MFI = c*StoneMod(logR,Kd,v,logKx,L0,biCoefMat);
            temp = mfiAdjMean(4*(whichR-1)+k,(4*(j-1)+1):(4*(j-1)+4));
            mean = meanPerCond(4*(whichR-1)+k,j);
            for l = 1:4
                logSqrErrMat(4*(whichR-1)+k,4*(j-1)+l) = ...
                    pseudoNormlike(temp(l),MFI,...
                    sigCoef*mean);
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