clc;clear;

%%%Establish constants
%Load data
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, ~, ~, best] = loadData;
%Valencies and TNP-X-BSA molarities
v = [4;26];
tnpbsa = [tnpbsa4;tnpbsa26];
%Create matrix of binomial coefficients
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

x = adiff(best);
errorAD = Error(x,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa)