clc; clear;

%Load the Kd values from Mimoto and Bruhns, the molarity of TNP-X-BSA used
%by Lux (see Figure 2), the normalized, background-MFI-adjusted MFIs from
%Lux for both TNP-X-BSAs, and the Kd values exclusively from Bruhns
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();
%TNP-X-BSA vector
tnpbsa = [tnpbsa4; tnpbsa26];
%Valency vector
v = [4; 26];

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 10
biCoefMat = zeros(10,10);
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
gs = GlobalSearch('StartPointsToRun','bounds','Display','iter');

problem = createOptimProblem('fmincon','objective',...
@(x) Error(x,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa),'x0',zeros(7,1),...
    'lb',(-10*ones(7,1)),'ub',10*ones(7,1),'options',opts);
[best, bsetFit, mfiExp] = run(gs,problem);

%Create residuals
mfiDiff = mfiExp - [mfiAdjMean4, mfiAdjMean26];

%Plotting the residuals: colored by FcgR, shape by IgG
for j = 1:6
    for k = 1:4
        if j == 1
            shape = 'b';
        elseif j == 2
            shape = 'g';
        elseif j == 3
            shape = 'r';
        elseif j == 4
            shape = 'c';
        elseif j == 5
            shape = 'm';
        else
            shape = 'k';
        end
        if k == 1
            color = 'o';
        elseif k == 2
            color = 'x';
        elseif k == 3
            color = 's';
        else
            color = 'd';
        end
        plot(((4*(j-1))+k)*ones(8,1),mfiDiff((4*(j-1))+k,:),[shape,color])
        hold on
    end
end