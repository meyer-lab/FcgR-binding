clear;clc;

%Load the Kd values from Mimoto and Bruhns, the molarity of TNP-X-BSA used
%by Lux (see Figure 2), the normalized, background-MFI-adjusted MFIs from
%Lux for both TNP-X-BSAs, and the Kd values exclusively from Bruhns
[kd, tnpbsa, mfiAdjMean, kdBruhns, ~, meanPerCond, stdPerCond] = loadData();
%Valency vector
v = [4; 26];
%Separate mean-adjusted MFIs into TNP-4-BSA data and TNP-26-BSA data
mfiAdjMean4 = mfiAdjMean(:,1:4);
mfiAdjMean26 = mfiAdjMean(:,5:8);

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Set up global solver. The vector being solved for is a seven-dimensional
%vector, the first six elements representing the expression levels of each 
%flavor of receptor and the seventh element representing a single, 
%universally-applied Kx, as described in Stone et al. All of these elements
%are such that, for any element x, 10^x equals the value it represents.
opts = optimoptions(@fmincon,'Algorithm','interior-point','Display','off');
gs = GlobalSearch('StartPointsToRun','bounds','Display','off');

problem = createOptimProblem('fmincon','objective',...
@(x) Error(x,kdBruhns,mfiAdjMean,v,biCoefMat,tnpbsa),'x0',zeros(9,1),...
    'lb',(-20*ones(9,1)),'ub',5*ones(9,1),'options',opts);
[best, bestFit,exitflag] = run(gs,problem);

[~,mfiExp] = Error(best,kdBruhns,mfiAdjMean,v,biCoefMat,tnpbsa);

%Create residuals
mfiDiff = mfiExp - mfiAdjMean;

%Calculating coefficients of determination for TNP-4-BSA and TNP-26-BSA.
%Note that all negative values in mfiAdjMean4 and mfiAdjMean26 were changed
%to zeros between lines 10 and 30.
CoefDet4 = 1 - nansum(nansum(mfiDiff(1:4,:).^2))/nansum(nansum((mfiAdjMean4 - nanmean(nanmean(mfiAdjMean4))).^2));
CoefDet26 = 1 - nansum(nansum(mfiDiff(5:8,:).^2))/nansum(nansum((mfiAdjMean26 - nanmean(nanmean(mfiAdjMean26))).^2));

%Plotting the residuals: colored by FcgR, shape by IgG
for j = 1:2
    for k = 1:4
        if j == 1
            color = 'b';
        else
            color = 'r';
        end
        if k == 1
            shape = 'o';
        elseif k == 2
            shape = 's';
        elseif k == 3
            shape = 'v';
        else
            shape = '^';
        end
        for l = 1:6
            plot((4*(l-1)+k)*ones(4,1),mfiDiff((4*(l-1))+k,(4*(j-1)+1):(4*j)),[shape,color])
            hold on
        end
    end
end
for j = 1:5
    plot((4*j+0.5)*ones(2,1),[-2.5,1],'k-')
    hold on
end