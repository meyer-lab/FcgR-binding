clear;clc;
%Load parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create matrix of binomial coefficients
%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Set options for genetic algorithm

%Set up genetic algorithm
[x,fval,exitflag,output,population,scores] = ga(@(x) ErrorAvidityChange(x,...
    kdBruhns,mfiAdjMean,biCoefMat,tnpbsa),11,[],...
    [],[],[],[-20;-20;-20;-20;-20;-20;-20;-20;-20;1;1],...
    [5;5;5;5;5;5;5;5;5;26;26],[],[10,11])