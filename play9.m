clear;clc;

[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

biCoefMat = zeros(30,30);
for j = 1:30
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

options = gaoptimset('Display','off');

[x,fval,exitflag,output,population,scores] = ga(@(x) -NormalErrorId(x,kdBruhns,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat),7,[],[],[],...
    [],[0,-20,-20,-20,1,1,-20],[6,0,5,5,30,30,2],[],[5 6]);

load('bestId.mat')
if fval < bestval
    bestval = fval;
    best = x;
    save('bestId.mat','best','bestval')
end