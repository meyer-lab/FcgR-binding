clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Load tempbest
load('best.mat')

%Load gong sound
load gong

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
%%%Note carefully that start is a row vector that must be transposed to be
%%%put into Error
start = best;
%standard deviation of exponential distribution
stdR = 0.85;
stdKx = 0.85;
stdc = 0.85;
stdsigma = 0.4;

%%%%Delete this


stdR = 2*stdR;
stdKx = 2*stdKx;
stdc = 2*stdc;
stdsigma = 4*stdsigma;

%%%%

%Number of samples for MCMC
nsamples = 100000;
%Log probability proposal distribution
%proppdf = @(x,y) -sum(([x(1:9), x(12:13)]-[y(1:9), y(12:13)]).^2);
% proppdf = @(x,y) 1/(1+max(10.^x1:6))-min(10.^x(1:6)));
proppdf = @(x,y) PROPPDF(x,y,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
    stdR,stdKx,stdc,stdsigma);
%Pseudo-random generator of new points to test; 0.039 gives accept of about
%0.23 for 7 parameters
proprnd = @(x) PROPRND(x,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
    stdR,stdKx,stdc,stdsigma);
%Probability distribution of interest
pdf = @(x) 0;

%Run Metropolis-Hastings algorithm
[sample,accept] = mhsample(start,nsamples,'logpdf',pdf,'logproppdf',proppdf, ...
    'proprnd',proprnd,'symmetric',0,'burnin',1000);

%Collect the errors for each element in the chain. Also, collect the list
%of all displacements in log space and "standard" space from the best fit
%point. From these displacements, find the distances in log space and in
%standard space.
distfrombest = zeros(nsamples,1);
for j = 1:nsamples
    distfrombest(j) = sum((best-sample(j,:)).^2);
end
testsample = sample;
testsample(:,1:9) = 10.^sample(:,1:9);
testsample(:,12) = 10.^sample(:,12);

for j = 1:12
    figure
    hist(sample(:,j),100);
end