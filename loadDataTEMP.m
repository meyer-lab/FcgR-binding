function output = loadDataTEMP(iter)
    %%% Load data from loadData
    [kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;
    
    %%% Reshape kaBruhns
    kaBruhns = kdBruhns(1:6,7:10);
    
    %%% Generate biCoefMat
    biCoefMat = zeros(30,30);
    for j = 1:30
        for k = 1:j
            biCoefMat(j,k) = nchoosek(j,k);
        end
    end
    
    %%% Iterate over the variable names
    
    if iter == 'ka'
        output = kaBruhns;
    elseif iter == 'tn'
        output = tnpbsa;
    elseif iter == 'mf'
        output = mfiAdjMean;
    elseif iter == 'me'
        output = meanPerCond;
    elseif iter == 'bi'
        output = biCoefMat;
    end
end