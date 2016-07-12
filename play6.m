clear;clc;

[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;
options = saoptimset('display','off');

[x,fval,exitflag,output] = ga(@(x) -NormalError(x,kdBruhns,...
    mfiAdjMean,tnpbsa,meanPerCond),13,[],[],[],[],[-20*ones(9,1);1;1;0;0],...
    [5*ones(9,1);4;26;25;25],[],[10 11]);

load gong
% load('y.mat')
% x = [y';0.1];
% 
% ntest = 1;
% while ntest
%     fval = NormalError(x, kdBruhns, mfiAdjMean, tnpbsa, meanPerCond);
%     if ~isnan(fval)
%         ntest = 0;
%         goodStart = x;
%         save('goodStart.mat','goodStart')
%     end
%     x(12) = rand;
% end

sound(y);