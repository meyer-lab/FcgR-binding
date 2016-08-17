function logprob = NormalErrorCnct2(Rtot,witchR)
    persistent tnpbsa mfiAdjMean kdBruhns meanPerCond biCoefMat whichR
    if nargin == 2
        [kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;
        whichR = witchR;
        
        biCoefMat = zeros(30);
        for j = 1:30
            for k = 1:j
                biCoefMat(k,j) = nchoosek(j,k);
            end
        end
        
        logprob = 0;
        return
    else
        if (max(isnan(Rtot)) == 1) || (max(isinf(Rtot)) == 1)
            logprob = -realmax/(1e20);
            return
        end
        for j = 5:6
            if Rtot(j) < 1
                Rtot(j) = 1;
            elseif Rtot(j) > 30
                Rtot(j) = 30;
            else
                Rtot(j) = floor(Rtot(j));
            end
        end
        logprob = NormalErrorCoef2_mex(Rtot,kdBruhns,mfiAdjMean,tnpbsa,...
            meanPerCond,biCoefMat,whichR);  
    end