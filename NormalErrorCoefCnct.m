function logprob = NormalErrorCnct(Rtot)
    persistent tnpbsa mfiAdjMean kdBruhns meanPerCond biCoefMat
    if nargin == 0
        [kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;
        
        biCoefMat = zeros(30);
        for j = 1:30
            for k = 1:j
                biCoefMat(k,j) = nchoosek(j,k);
            end
        end
        
        logprob = 0;
        return
    else
        if max(isnan(Rtot)) == 1
            logprob = -1e6;
            return
        end
        for j = 10:11
            if Rtot(j) < 1
                Rtot(j) = 1;
            elseif Rtot(j) > 30
                Rtot(j) = 30;
            else
                Rtot(j) = floor(Rtot(j));
            end
        end
        logprob = NormalErrorCoef_mex(Rtot,kdBruhns,mfiAdjMean,tnpbsa,...
            meanPerCond,biCoefMat);  
    end