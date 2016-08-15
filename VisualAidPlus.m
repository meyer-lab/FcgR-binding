clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(30,30);
for m = 1:30
    for n = 1:m
        biCoefMat(n,m) = nchoosek(m,n);
    end
end

%Set up options for simulated annealing
options = saoptimset('display','off');

%Run simulated annealing for each pair of FcgRs
bigDiff = zeros(3,6,6);
Diff = zeros(6,6);
check = zeros(6,6);
logRvec = 2:0.5:7;
Lvec = -14:0;

VisAidPlusCell = {};
for j = length(logRvec)
    VisAidPlusCellIn = {};
    for k = length(Lvec)
        VisAidCellInin = {};
        for l = 1:3
            for m = 1:6
                for n = 1:6
                    if m == n
                        bigDiff(2:3,m,n) = NaN*ones(2,1);
                        Diff(m,n) = NaN;
                    else
                        [x,fval,exitflag,output] = simulannealbnd(@(x) -playSimAnneal(x,...
                            kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,m,n,l),[4,26,5],...
                            [1,1,-20],[4,26,5],options);
                        bigDiff(:,m,n) = x;
                        Diff(m,n) = fval;
%                         check(k,l) = exitflag;
                    end
                end
            end
            if l == 1
                VisAidCellInin.bigDiffLigand = bigDiff;
                VisAidCellInin.DiffLigand = -Diff;
            elseif l == 2
                VisAidCellInin.bigDiffRmulti = bigDiff;
                VisAidCellInin.DiffRmulti = -Diff;
            else
                VisAidCellInin.bigDiffCluster = bigDiff;
                VisAidCellInin.DiffCluster = -Diff;
            end
        end
        temptempName = num2str(Lvec(k));
        if temptempName(1) == '-'
            temptempName(1) = 'n';
        end
        tempName = ['L1e' temptempName];
        eval(['VisAidCellIn.' tempName ' = VisAidCellInin;']);
    end
    temptempName = num2str(logRvec(j));
    if temptempName(1) == '-'
            temptempName(1) = 'n';
    end
    tempName = ['logR1e' temptempName];
    eval(['VisAidCell.' tempName ' = VisAidCellIn;']);
end

VisAidPlusCell = VisAidCell;
save('VisAidPlusCell.mat','VisAidPlusCell')