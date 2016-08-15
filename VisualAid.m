clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(30,30);
for k = 1:30
    for l = 1:k
        biCoefMat(l,k) = nchoosek(k,l);
    end
end

%Set up options for simulated annealing
options = gaoptimset('display','off');

%Run simulated annealing for each pair of FcgRs
bigDiff = zeros(3,6,6);
Diff = zeros(6,6);
check = zeros(6,6);
for j = 1:3
    for k = 1:6
        for l = 1:6
            if k == l
                bigDiff(2:3,k,l) = NaN*ones(2,1);
                Diff(k,l) = NaN;
            else
                [x,fval,exitflag,output] = ga(@(x) playSimAnneal(x,...
                    kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,k,l,j),3,[],...
                    [],[],[],[1,1,-20],[4,30,-1],[],[1 2],options);
                bigDiff(:,k,l) = x;
                Diff(k,l) = fval;
%                 check(k,l) = exitflag;
            end
        end
    end
    if j == 1
        bigDiffLigand = bigDiff;
        DiffLigand = Diff;
    elseif j == 2
        bigDiffRmulti = bigDiff;
        DiffRmulti = Diff;
    else
        bigDiffCluster = bigDiff;
        DiffCluster = Diff;
    end
end

save('DiffCompare.mat','bigDiffLigand','bigDiffRmulti','bigDiffCluster',...
    'DiffLigand','DiffRmulti','DiffCluster')