clear;clc;
close all
disp(0)

logKd = [-20:0.5:(-2)];
sz = length(logKd);
logL = -8;
logR = log10(2e5);

diffL = zeros(sz);
diffRmulti = diffL;
diffParamL = zeros(2,sz,sz);
diffParamRmulti = diffParamL;

options = gaoptimset('display','off');

for j = 1:sz
    for k = 1:sz
        if j ~= k
            [x,diffL(j,k)] = ga(@(x) -deletesoon2(logKd(j),logKd(k),x(1),x(2),...
                logL,logR,'L'),2,[],[],[],[],[1 -20],[30 -2],[],1,options);
            diffParamL(:,j,k) = x';
            [x,diffRmulti(j,k)] = ga(@(x) -deletesoon2(logKd(j),logKd(k),x(1),x(2),...
                logL,logR,'Rmulti'),2,[],[],[],[],[1 -20],[30 -2],[],1,options);
            diffParamRmulti(:,j,k) = x';
        else
            diffParamL(:,j,k) = [nan;nan];
            diffParamRmulti(:,j,k) = [nan;nan];
        end
    end
    clc;
    disp(j/sz*100)
end
diffL = -diffL;
diffRmulti = -diffRmulti;

save('exploratorya.mat','diffParamL','diffParamRmulti','diffL',...
    'diffRmulti','sz','logKd')