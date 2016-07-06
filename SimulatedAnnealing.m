%Runs a simulated annealing algorithm on the exponentiation of the output
%of PDF

clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Load x and y
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

options = saoptimset('display','off');
%Run simulated annealing
[x,fval,exitflag,output] = simulannealbnd(@(x) -PDF(x,kdBruhns,...
    mfiAdjMean,biCoefMat,tnpbsa,...
    meanPerCond,stdPerCond),ones(1,11),[-20*ones(1,9),1,1],...
    [5*ones(1,9),5,26],options);