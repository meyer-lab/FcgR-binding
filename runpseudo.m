clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

nsamples = 10000;
goodsize = 3;
mehsize = 10;

[good,goodfit,meh] = pseudoAlgorithm_mex(nsamples,goodsize,mehsize,...
    kdBruhns,tnpbsa,mfiAdjMean,best,meanPerCond,stdPerCond,biCoefMat);