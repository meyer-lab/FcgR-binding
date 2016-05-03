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

%Set up parameters for GlobalSearch and fmincon

Rc = zeros(7, 10);
RcFit = zeros(1,size(Rc,2));

opts = optimoptions(@fmincon,'Algorithm','interior-point','Display','off');
gs = GlobalSearch('StartPointsToRun','bounds','Display','iter');

for j = 1:10
    
    problem = createOptimProblem('fmincon','objective',...
    @(x) Error(x,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa),'x0',zeros(7,1),...
        'lb',(-10*ones(7,1)),'ub',10*ones(7,1),'options',opts);
    [Rc(:,j), RcFit(j)] = run(gs,problem);
        
    %From all best fits from v = 1 to v = 10, find the value of v and its
    %corresponding vector R which yield the least summed squared error
    [~, IDX] = min(RcFit);
    best = [Rc(:,IDX);IDX];
    
    %Results for MFI per flavor of receptor per flavor of immunoglobulin
    %that we would expect based on our optimization
    [~, mfiExp] = Error(best(1:size(best,1)-1),kdBruhns,mfiAdjMean4,mfiAdjMean26,best(8),biCoefMat,tnpbsa);
end
mfiDiff = [mfiExp(:,1:4) - mfiAdjMean4, mfiExp(:,5:8) - mfiAdjMean26];