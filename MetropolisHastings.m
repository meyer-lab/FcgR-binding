clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Load x and y and swag
load('x.mat')
load('y.mat')

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%%%Note carefully that start is a row vector that must be transposed to be
%%%put into Error
% start = [25*rand(1,9)-20,4,8];
start = y;
% start(1:9) = -10*ones(1,9);
%Number of samples for MCMC
nsamples = 10000;
%Log probability proposal distribution
proppdf = @(x,y) -sum((x(1:9)-y(1:9)).^2);
%Pseudo-random generator of new points to test; 0.039 gives accept of about
%0.23 for 7 parameters
proprnd = @(x) PROPRND(x);
%Probability distribution of interest
pdf = @(x) PDF_mex(x,kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,meanPerCond,stdPerCond);

%Run Metropolis-Hastings algorithm
[sample,accept] = mhsample(start,nsamples,'logpdf',pdf,'logproppdf',proppdf, ...
    'proprnd',proprnd,'symmetric',0,'burnin',1000);

%Collect the errors for each element in the chain. Also, collect the list
%of all displacements in log space and "standard" space from the best fit
%point. From these displacements, find the distances in log space and in
%standard space.
AICs = zeros(nsamples,1);
errors = AICs;
mfiExps = zeros(24,8,nsamples);
% dispFromBest = zeros(size(sample));
% distFromBest = zeros(nsamples,1);
% rdispFromBest = zeros(size(sample));
% rdistFromBest = zeros(nsamples,1);
for j = 1:nsamples
    AICs(j) = PDF_mex(sample(j,:),kdBruhns, mfiAdjMean,biCoefMat,tnpbsa,....
        meanPerCond,stdPerCond);
    [errors(j),mfiExps(:,:,j)] = ErrorAvidityChange(sample(j,:)',kdBruhns,....
        mfiAdjMean,biCoefMat,tnpbsa);
%     dispFromBest(j,:) = best' - sample(j,:);
%     distFromBest(j) = sqrt(nansum(dispFromBest(j,:).^2));
%     rdispFromBest(j,:) = 10.^best' - 10.^sample(j,:);
%     rdistFromBest(j) = sqrt(nansum(rdispFromBest(j,:).^2));
end

testsample = sample;
testsample(1:9) = 10.^sample(1:9);