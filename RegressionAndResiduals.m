clc; clear;

cluster = parcluster('local');
cluster.NumWorkers = 5;

parpool(5);

%Load the Kd values from Mimoto and Bruhns, the molarity of TNP-X-BSA used
%by Lux (see Figure 2), the normalized, background-MFI-adjusted MFIs from
%Lux, and the Kd values exclusively from Bruhns
[kd, tnpbsa4, tnpbsa26 mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 10
biCoefMat = zeros(10,10);
for k = 1:10
    for j = 1:k
        biCoefMat(j,k) = nchoosek(k,j);
    end
end

%Set up parameters for GlobalSearch and fmincon

Rc = zeros(9, 10);
RcFit = zeros(1,size(Rc,2));

opts = optimoptions(@fmincon,'Algorithm','interior-point','Display','off','UseParallel',true);
gs = GlobalSearch('StartPointsToRun','bounds','Display','off');

for j = 1:2
    if j == 1
        mfiAdjMean = mfiAdjMean4;
    else
        mfiAdjMean = mfiAdjMean26;
    end
    for k = 1:size(Rc,2)
        problem = createOptimProblem('fmincon','objective',...
        @(x) Error(x,kdBruhns,mfiAdjMean,k,biCoefMat),'x0',ones(8,1),...
            'lb',(-10*ones(8,1)),'ub',10*ones(8,1),'options',opts);
        [Rc(1:8,k), RcFit(k)] = run(gs,problem);
        Rc(9,k) = k;
    end
    
    %From all best fits from v = 1 to v = 10, find the value of v and its
    %corresponding vector R which yield the least summed squared error
    [~, IDX] = min(RcFit);
    best = Rc(:,IDX);
    
    %Results for MFI per flavor of receptor per flavor of immunoglobulin
    %that we would expect based on our optimization
    [~, mfiExp] = Error(best(1:size(best,1)-1),kdBruhns,mfiAdjMean,best(9),biCoefMat);

    if j == 1
        mfiExp4 = mfiExp;
        Rc4 = Rc;
        RcFit4 = RcFit;
        best4 = best;
    else
        mfiExp26 = mfiExp;
        Rc26 = Rc;
        RcFit26 = RcFit;
        best26 = best;
    end
end

%Calculate the residuals against the model for both the TNP-4-BSA data and
%the TNP-26-BSA data
mfiDiff4 = mfiExp4 - mfiAdjMean4;
mfiDiff26 = mfiExp26 - mfiAdjMean26;

delete(gcp('nocreate'));