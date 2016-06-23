[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, ... 
    bestHomogeneicFit, bestHomogeneicKx, best, meanPerCond, stdPerCond] = loadData()

biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

v = [4;26];
tnpbsa = [tnpbsa4;tnpbsa26];
PDF(best,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa,meanPerCond,stdPerCond)