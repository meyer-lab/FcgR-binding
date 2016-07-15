clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Load tempbest
load('tempbest.mat')

%Load gong sound
load gong

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(30,30);
for j = 1:30
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%%%Note carefully that start is a row vector that must be transposed to be
%%%put into Error
start = ones(1,7);
start(5:6) = [4 26];
% start(1:9) = -10*ones(1,9);
%Number of samples for MCMC
nsamples = 100000;
%Log probability proposal distribution
%proppdf = @(x,y) -sum(([x(1:9), x(12:13)]-[y(1:9), y(12:13)]).^2);
proppdf = @(x,y) 1;
%Pseudo-random generator of new points to test; 0.039 gives accept of about
%0.23 for 7 parameters
proprnd = @(x) PROPRND2(x);
%Probability distribution of interest
pdf = @(x) NormalErrorId_mex(x,kdBruhns,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat);

%Run Metropolis-Hastings algorithm
[sample,accept] = mhsample(start,nsamples,'logpdf',pdf,'proppdf',proppdf, ...
    'proprnd',proprnd,'symmetric',0,'burnin',1000);

%Collect the errors for each element in the chain. Also, collect the list
%of all displacements in log space and "standard" space from the best fit
%point. From these displacements, find the distances in log space and in
%standard space.
likelihoods = zeros(nsamples,1);
for j = 1:nsamples
    likelihoods(j) = NormalErrorId(sample(j,:),kdBruhns,mfiAdjMean,tnpbsa,...
        meanPerCond,biCoefMat);
end
testsample = sample;
testsample(:,1:4) = 10.^sample(:,1:4);
testsample(:,7) = 10.^sample(:,7);

sound(y);