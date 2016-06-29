%%%%IMPORTANT!!! This script runs itself at the end, causing an infinite
%%%%loop. Quit script after a minute or so and see the values saved in
%%%%y.mat.

clear;clc;
%Load parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;
load('z.mat')

%Create matrix of binomial coefficients
%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

options = gaoptimset('Generations',10000);

[x, fval,exitflag,output,population,scores] = ga(@(x) -PDF(x,kdBruhns,...
    mfiAdjMean,biCoefMat,tnpbsa,...
    meanPerCond,stdPerCond),6,[],[],[],[],[-20,-20,-20,-20,1,1],...
    [5,5,5,5,4,26],[],[5,6],options);

xTrue = x;
xTrue(1) = 10.^x(1);

if -PDF(z,kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,meanPerCond,stdPerCond) > fval
    z = x;
    zval = fval;
    save('z.mat','z','zval')
end

run GeneticAlgorithm