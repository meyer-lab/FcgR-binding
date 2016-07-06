clear;clc;

%For fun
load gong

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

%Load aicbest; this is the point which yields the lowest AIC with both
%simulated annealing and MATLAB's genetic algorithm. This is to get the
%best fits for the TNP-BSA-to-MFI conversion factors
% load('aicbest.mat')
% %Common logs of TNP-BSA-to-MFI conversion factors
% convfac = aicbest(8:9)';
convfac = [1;1];

%Dimensions correspond to IgG, FcgR, FcgR (the repeat is intentional; see
%below), TNP-BSA avidity, and Kx, respectively. The script will pore 
%through Kx values by integer order of magnitude ranging from -10 to -3.
%
%Each matrix "cross-section" by dimensions 2 and 3 of either 5-tensor
%utilTens shows the difference (A and C) or difference in order of 
%magnitude (B and D) of either the number of ligand bound (A and B) or the
%number of dimers formed (C and D0 at equilibrium under the conditions
%indicated by the values in dimensions 1, 4, and 5.
utilTensA = zeros(4,6,6,26,8);
utilTensB = utilTensA;
utilTensC = utilTensA;
utilTensD = utilTensA;

%Vector representing Kx orders of magnitude
ordmagKx = [-10:-3];

%Iterate through TNP-4-BSA avidities, TNP-26-BSA avidities, and Kx orders
%of magnitude. I assume that there are 1000 of each FcgR on the cell.
for j = 1:26
    for k = 1:8
        x = [3*ones(6,1);ordmagKx(k);convfac;1;j];
        [~,~,mfiExpPre] = ErrorAvidityChange(x,kdBruhns,...
            mfiAdjMean,biCoefMat,tnpbsa);
        DimerMat = DimerFinder(x,kdBruhns,...
            mfiAdjMean,biCoefMat,tnpbsa);
        for l = 1:4
            tempMatA = zeros(6);
            tempMatB = tempMatA;
            tempMatC = tempMatA;
            tempMatD = tempMatA;
            for m = 1:6
                for n = 1:6
                    tempMatA(m,n) = mfiExpPre(m,l+4) - mfiExpPre(n,l+4);
                    tempMatB(m,n) = log10(mfiExpPre(m,l+4)/mfiExpPre(n,l+4));
                    tempMatC(m,n) = DimerMat(m,l+4) - DimerMat(n,l+4);
                    tempMatD(m,n) = log10(DimerMat(m,l+4)/DimerMat(n,l+4));
                end
            end
            utilTensA(l,:,:,j,k) = tempMatA;
            utilTensB(l,:,:,j,k) = tempMatB;
            utilTensC(l,:,:,j,k) = tempMatC;
            utilTensD(l,:,:,j,k) = tempMatD;
        end
    end
end
% 
% for j = 1:26
%     for k = 1:8
%         for l = 1:4
%             bar3(permute(utilTensD(l,:,:,j,k),[2 3 1]));
%             pause
%         end
%     end
% end

utilTensA = permute(utilTensA,[2 3 1 4 5]);
utilTensB = permute(utilTensB,[2 3 1 4 5]);
utilTensC = permute(utilTensC,[2 3 1 4 5]);
utilTensD = permute(utilTensD,[2 3 1 4 5]);
utilMat = zeros(30,832);
%Change the following to change what is being compared through the script
utilTens = utilTensB;

for j = 1:4
    for k = 1:26
        for l = 1:8
            utilMat(:,208*(j-1)+8*(k-1)+l) = [utilTens(1,2:6,j,k,l),...
                utilTens(2,3:6,j,k,l),utilTens(3,4:6,j,k,l),...
                utilTens(4,5:6,j,k,l),utilTens(5,6,j,k,l),...
                utilTens(2,1,j,k,l),utilTens(3,1:2,j,k,l),...
                utilTens(4,1:3,j,k,l),utilTens(5,1:4,j,k,l),...
                utilTens(6,1:5,j,k,l)]';
        end
    end
end

%Transpose for sake of ease in using DBSCAN
utilMat = utilMat';
% [IDX,isnoise] = DBSCAN(utilMat,15,16);

%Find all differences in order of magnitude of ligand bound greater than or
%equal to 2
testsignificance = (utilMat >= 1);

goodcomboPre = [];

for j = 1:832
    for k = 1:30
        if testsignificance(j,k) == 1
            goodcomboPre = [goodcomboPre [j;k]];
        end
    end
end

%Matrices to help convert [j;k] column vectors in goodcomboPre to indices
%in utilTensB
convertj = zeros(3,832);
for j = 1:4
    for k = 1:26
        for l = 1:8
            convertj(:,208*(j-1)+8*(k-1)+l) = [j;k;l];
        end
    end
end
convertk = [[1;2] [1;3] [1;4] [1;5] [1;6] [2;3] [2;4] [2;5] [2;6]...
    [3;4] [3;5] [3;6] [4;5] [4;6] [5;6] [2;1] [3;1] [3;2] [4;1] [4;2]...
    [4;3] [5;1] [5;2] [5;3] [5;4] [6;1] [6;2] [6;3] [6;4] [6;5]];

sizegoodcombo = size(goodcomboPre,2);
goodcombo = zeros(5,sizegoodcombo);
for j = 1:sizegoodcombo
    goodcombo(:,j) = [convertj(:,goodcomboPre(1,j));...
        convertk(:,goodcomboPre(2,j))];
end
tester = [];

for j = 1:sizegoodcombo
    measure = goodcombo(3:5,j);
    test = 1;
    for k = 1:size(tester,2)
        if tester(:,k) == measure
            test = 0;
        end
    end
    if test == 1
        tester = [tester measure];
    end
end

sizetester = size(tester,2);
tester2 = [];

for j = 1:sizetester
    measure = tester(2:3,j);
    test = 1;
    for k = 1:size(tester2,2)
        if tester2(:,k) == measure
            test = 0;
        end
    end
    if test == 1
        tester2 = [tester2 measure];
    end
end

finalIter = size(tester2,2);
%Create a permutation of utilTens for ease's sake
helpfulTens = permute(utilTens,[4 3 1 2 5]);

% for j = 1:finalIter
%     for k = 1:8
%         plot(helpfulTens(:,:,tester2(1,j),tester2(2,j),k));
%         pause
%     end
%     sound(y);
% end

%In the third dimensions of bestcombo, the first value represents the IgG,
%the second the valence, the third the index of ordmagKx, and the fourth
%the value of utilTens at the corresponding indices
bestcombo = zeros(6,6,4);
for j = 1:6
    for k = 1:6
        [temp,idx1] = max(utilTens(j,k,:,:,:));
        [temp,idx2] = max(temp);
        [temp,idx3] = max(temp);
        bestcombo(j,k,4) = temp;
        bestcombo(j,k,3) = idx3;
        derp = idx2(1,1,1,1,idx3);
        bestcombo(j,k,2) = derp;
        bestcombo(j,k,1) = idx1(1,1,1,derp,idx3);
    end
end

presimilMat = [];
similMat = [];
for j = 1:6
    for k = 1:6
        if j ~= k
            temp = permute(bestcombo(j,k,:),[3 1 2]);
            presimilMat = [presimilMat temp];
            test = 1;
            if ~isempty(similMat)
                for l = 1:size(similMat,2)
                    if temp == similMat(:,l)
                        test = 0;
                    end
                end
            end
            if test == 1
                similMat = [similMat permute(bestcombo(j,k,:),[3 1 2])];
            end
        end
    end
end

plot(presimilMat(1:3,:)')

kdCompare = zeros(4,6,6);
kdCompareBar = zeros(6);
for j = 1:6
    for k = 1:6
        for l = 1:4
            kdCompare(l,j,k) = log10(kdBruhns(j,l)/kdBruhns(k,l));
            [~, kdCompareBar(j,k)] = max(kdCompare(:,j,k));
        end
    end
end
figure
bar3(kdCompareBar)