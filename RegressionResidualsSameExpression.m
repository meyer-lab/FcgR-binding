%clc; clear;

%Load the Kd values from Mimoto and Bruhns, the molarity of TNP-X-BSA used
%by Lux (see Figure 2), the normalized, background-MFI-adjusted MFIs from
%Lux for both TNP-X-BSAs, and the Kd values exclusively from Bruhns
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();
%TNP-X-BSA vector
tnpbsa = [tnpbsa4; tnpbsa26];
%Valency vector
v = [4; 26];

%Changing negative background-adjusted MFIs to zeros
for j = 1:24
    for k = 1:4
        if mfiAdjMean4(j,k) < 0
            mfiAdjMean4(j,k) = 0;
        end
        if mfiAdjMean26(j,k) < 0
            mfiAdjMean26(j,k) = 0;
        end
    end
end

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
@(x) ErrorSameExpression(x,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa),'x0',zeros(2,1),...
    'lb',(-10*ones(2,1)),'ub',10*ones(2,1),'options',opts);
[best, bestFit] = run(gs,problem);

[~,mfiExp] = ErrorSameExpression(best,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa);

%Create residuals
mfiDiff = mfiExp - [mfiAdjMean4, mfiAdjMean26];

%Calculating coefficients of determination for TNP-4-BSA and TNP-26-BSA
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