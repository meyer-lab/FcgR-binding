clc; clear;

%Load the Kd values from Mimoto and Bruhns, the molarity of TNP-X-BSA used
%by Lux (see Figure 2), the normalized, background-MFI-adjusted MFIs from
%Lux, and the Kd values exclusively from Bruhns
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();

tnpbsa = [tnpbsa4; tnpbsa26];

v = [4; 26];

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 10
biCoefMat = zeros(10,10);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

opts = optimoptions(@fmincon,'Algorithm','interior-point','Display','off');
gs = GlobalSearch('StartPointsToRun','bounds','Display','iter');

problem = createOptimProblem('fmincon','objective',...
@(x) Error(x,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa),'x0',zeros(7,1),...
    'lb',(-10*ones(7,1)),'ub',10*ones(7,1),'options',opts);
[best, bsetFit, mfiExp] = run(gs,problem);

mfiDiff = mfiExp - [mfiAdjMean4, mfiAdjMean26];