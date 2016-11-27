function data = loadDataINTERFACE(ind)
    [kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData();
    if ind == 1
        data = mfiAdjMean;
    elseif ind == 2
        data = tnpbsa;
    elseif ind == 3
        data = kdBruhns;
    elseif ind == 4
        data = meanPerCond;
    elseif ind == 5
        data = biCoefMat;
    end
end