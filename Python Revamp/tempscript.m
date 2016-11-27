function logSqrErr = tempscript()

[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData();

biCoefMat = zeros(30);
for j = 1:30
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

logSqrErr = NormalErrorCoef(ones(1,12), kdBruhns, mfiAdjMean, tnpbsa,...
    meanPerCond, biCoefMat);

end