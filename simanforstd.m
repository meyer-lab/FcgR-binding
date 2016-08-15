clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Load tempbest
load('best.mat')

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 30
biCoefMat = zeros(30,30);
for j = 1:30
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Lower and upper bounds of various parameters
lbR = 0;
ubR = 8;
lbKx = -20;
ubKx = 0;
lbc = -20;
ubc = 5;
lbv = 1;
ubv = 30;
lbsigma = -20;
ubsigma = 2;

%Number of samples for MCMC
nsamples = 1000;

options = optimoptions('simulannealbnd','display','off');

[x, fval] = simulannealbnd(@(x) -tempforstd(x,best,tnpbsa,mfiAdjMean,...
    kdBruhns,meanPerCond,stdPerCond,biCoefMat,lbR,ubR,lbKx,ubKx,lbc,ubc,...
    lbv,ubv,lbsigma,ubsigma,nsamples),[0.4 0.6 0.2 0.01],zeros(1,4),...
    20*ones(1,4),options);