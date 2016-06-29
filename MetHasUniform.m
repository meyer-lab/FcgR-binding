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

start = [25*rand(1,4)-20,1,1];

nsamples = 10000;

proppdf = @(x,y) -(x(1)-y(1))^2;

proprnd = @(x) PROPRND2(x);

pdf = @(x) PDF(x,kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,meanPerCond,stdPerCond);

%Run Metropolis-Hastings algorithm
[sample,accept] = mhsample(start,nsamples,'logpdf',pdf,'logproppdf',proppdf, ...
    'proprnd',proprnd,'symmetric',0,'burnin',0);

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
    AICs(j) = PDF(sample(j,:),kdBruhns, mfiAdjMean,biCoefMat,tnpbsa,....
        meanPerCond,stdPerCond);
    [errors(j),mfiExps(:,:,j)] = ErrorAvidityChange(sample(j,:)',kdBruhns,....
        mfiAdjMean,biCoefMat,tnpbsa);
%     dispFromBest(j,:) = best' - sample(j,:);
%     distFromBest(j) = sqrt(nansum(dispFromBest(j,:).^2));
%     rdispFromBest(j,:) = 10.^best' - 10.^sample(j,:);
%     rdistFromBest(j) = sqrt(nansum(rdispFromBest(j,:).^2));
end

testsample = sample;
testsample(1:4) = 10.^sample(1:4);

load handel
sound(y,Fs);