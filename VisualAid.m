clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Set up options for simulated annealing
options = saoptimset('display','off');

%Run simulated annealing for each pair of FcgRs
bigDiff = zeros(3,6,6);
Diff = zeros(6,6);
check = zeros(6,6);
for j = 1:6
    for k = 1:6
        if j == k
            bigDiff(2:3,j,k) = NaN*ones(2,1);
            Diff(j,k) = NaN;
        else
            [x,fval,exitflag,output] = simulannealbnd(@(x) -playSimAnneal(x,...
                kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,j,k),[4,26,5],...
                [1,1,-20],[4,26,5],options);
            bigDiff(:,j,k) = x;
            Diff(j,k) = fval;
            check(j,k) = exitflag;
        end
    end
end
figure
bar3(-Diff)