clear;clc;

[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, ~, ~, best, meanPerCond, stdPerCond] = loadData;

biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

PDF(best,kdBruhns,mfiAdjMean4,mfiAdjMean26,[4;26],biCoefMat,[tnpbsa4;tnpbsa26], meanPerCond, stdPerCond)