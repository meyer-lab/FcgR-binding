clear;clc;

%%%Load parameters
load('Nonuni,choline.mat')
%This is the output of the Error function at best fit, using data
%normalized by CHO line and assuming receptor expression is nonuniform
minError = bestFit;

load('Nonuni,column.mat')
%This is the best fit that results from normalizing by column and assuming
%receptor expression is nonuniform
start = best;

%Loading basic parameters
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, bestHomogeneicFit, bestHomogeneicKx] = loadData;

%Set valencies
v = [4;26];
%Create vector of TNP-BSA molarities
tnpbsa = [tnpbsa4;tnpbsa26];
%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end


%Set up MCMC
mcmcs = 10000;
markov = zeros(7,mcmcs);

%Set up initial guess
% markov(:,1) = start;
markov(:,1) = zeros(7,1);

%Run MCMC
prevError = Error(markov(:,1), kdBruhns, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa);
for j = 2:mcmcs
    new = log10(rand)+1;
    newError = Error(new, kdBruhns, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa);
    if rand < min([1,exp((prevError-newError)/2)])
        markov(:,j) = new;
        prevError = newError;
    else
        markov(:,j) = markov(:,j-1);
    end
end