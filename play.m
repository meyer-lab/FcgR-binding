[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData()

biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

v = [4;26];
PDF(best,kdBruhns,mfiAdjMean,v,biCoefMat,tnpbsa,meanPerCond,stdPerCond)