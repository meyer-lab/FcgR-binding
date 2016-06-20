clc; clear;

%Load the Kd values from Mimoto and Bruhns, the molarity of TNP-X-BSA used
%by Lux (see Figure 2), the normalized, background-MFI-adjusted MFIs from
%Lux for both TNP-X-BSAs, and the Kd values exclusively from Bruhns
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();
%TNP-X-BSA vector
tnpbsa = [tnpbsa4; tnpbsa26];

% % %Find the expression levels which best fit for each plausible pair of
% % %TNP-4-BSA valency and TNP-26-BSA valency, such that the correct valencies
% % %might be known.

% Matrix of best-fit parameters
bestFitMat = zeros(4,26);
% 3-Tensor of best-fit parameters
bestTensor = zeros(4,26,7);
% 4-Tensor of residuals
mfiDiffTensor = zeros(4,26,24,8);
for j = 1:4
    for k = 1:26
        %Valency vector
        v = [j; k];
        
        %Changing negative background-adjusted MFIs to zeros
        for l = 1:24
            for m = 1:4
                if mfiAdjMean4(l,m) < 0
                    mfiAdjMean4(l,m) = 0;
                end
                if mfiAdjMean26(l,m) < 0
                    mfiAdjMean26(l,m) = 0;
                end
            end
        end
        
        %Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
        %all i from 1 to v for all v from 1 to 26
        biCoefMat = zeros(26,26);
        for l = 1:26
            for m = 1:l
                biCoefMat(m,l) = nchoosek(l,m);
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
        @(x) Error(x,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa),'x0',zeros(7,1),...
            'lb',(-10*ones(7,1)),'ub',10*ones(7,1),'options',opts);
        [best, bestFit] = run(gs,problem);
        
        [~,mfiExp] = Error(best,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa);
        
        %Create residuals
        mfiDiff = mfiExp - [mfiAdjMean4, mfiAdjMean26];
        
        % Update data tensors
        bestFitMat(j,k) = bestFit;
        bestTensor(j,k,:) = best;
        mfiDiffTensor(j,k,:,:) = mfiDiff;
    end
end