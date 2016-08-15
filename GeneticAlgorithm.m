clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Load tempbest
load('tempbest.mat')

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

options = gaoptimset('display','off');

load('best.mat')

for j = 1:30
    [x fval] = ga(@(x) -NormalError_mex(x,kdBruhns,mfiAdjMean,tnpbsa,...
        meanPerCond,biCoefMat),12,[],[],[],[],[lbR*ones(1,6) lbKx lbc*ones(1,2)...
        1 1 lbsigma],[ubR*ones(1,6) ubKx ubc*ones(1,2) ubv*ones(1,2) ubsigma],...
        [],[10 11],options);
    if fval < bestval
        bestval = fval;
        best = x;
        save('best.mat','best','bestval')
    end
end
'DONE!!!'