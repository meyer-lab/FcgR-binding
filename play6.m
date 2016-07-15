clear;clc;

[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;
options = saoptimset('display','off');

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

load('tempbest.mat')

[x,fval,exitflag,output] = ga(@(x) -NormalError(x,kdBruhns,...
    mfiAdjMean,tnpbsa,meanPerCond,biCoefMat),13,[],[],[],[],[-20*ones(9,1);1;1;-6;-6],...
    [5*ones(9,1);4;26;2;2],[],[10 11]);

if fval < fvalBest
    tempbest = x;
    fvalBest = fval;
    save('tempbest.mat','tempbest','fvalBest')
end
run play6


% load gong
% load('y.mat')
% x = [y';0.1;0.1];
% 
% ntest = 1;
% while ntest
%     fval = NormalError(x, kdBruhns, mfiAdjMean, tnpbsa, meanPerCond);
%     if ~isnan(fval)
%         ntest = 0;
%         goodStart = x;
%         save('goodStart.mat','goodStart')
%     end
%     x(12:13) = rand(2,1);
% end

% load('tempbest.mat')

% NormalError(tempbest,kdBruhns,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat);
% NormalError_mex(tempbest,kdBruhns,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat);
