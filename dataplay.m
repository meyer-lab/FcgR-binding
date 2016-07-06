clear;clc;

%load data from the 4 million sample run of MetropolisHastings
load('mhsampleResults.mat')

Zpca = myPCA(normtestsample',11);

temp = corrcoef([Zpca',normtestsample]);

temp(1:11,1:11) = zeros(11);

bar3(temp)