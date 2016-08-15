clear;
% Lower and upper bounds of various parameters
lbR = 0;
ubR = 8;
lbKx = -20;
ubKx = 0;
lbc = -20;
ubc = 5;
lbv = 1;
ubv = 30;
lbsigma = -20;
ubsigma = 2;

% Create intervals of state space search using parameter bounds; 3 per
% analog parameter and 10 for each avidity
Riss = lbR:(ubR-lbR)/9:ubR;
Kxiss = lbKx:(ubKx-lbKx)/9:ubKx;
viss = 1:29/5:30;
viss = ceil(viss);

RissL = length(Riss);
vissL = length(viss);

% Create a cell which will hold cells of the same structure for each FcgR
SpaceExplorer2cell = cell(1,6);

% Set up options for genetic algorithm
options = gaoptimset('display','off');

% For each FcgR
for j = 1:6
    % Initialize persistent variables in NormalErrorCoefCnct2
    NormalErrorCoefCnct2(ones(1,7),j);
    
    %Set up cell arrays of tentative global optima and their log-likelihoods
    ptent = cell(RissL-1,RissL-1,vissL-1,vissL-1);
    lntent = ptent;

    % Iterate over each parameter range and find global optimum
    for k = 1:(RissL-1)
        lbR = Riss(k);
        ubR = Riss(k+1);
        for l = 1:(RissL-1)
            lbKxcoef = Kxiss(l);
            ubKxcoef = Kxiss(l+1);
            for m = 1:(vissL-1)
                lbv1 = viss(m);
                ubv1 = viss(m+1);
                for n = 1:(vissL-1)
                    lbv2 = viss(n);
                    ubv2 = viss(n+1);

                    [x,fval] = ga(@(x) -NormalErrorCoefCnct2(x),...
                        7,[],[],[],[],[lbR lbKxcoef lbc lbc lbv1 lbv2...
                        lbsigma],[ubR ubKxcoef ubc ubc ubv1 ubv2 ubsigma],...
                        [],[5 6], options);
                    ptent{k,l,m,n} = x;
                    lntent{k,l,m,n} = -fval;
                end
            end
        end
    end
    SpaceExplorer2cell{j} = {ptent lntent};
end
save('SpaceExplorer2Data.mat','RissL','vissL','SpaceExplorer2cell')

disp('SpaceExplorer2 complete.')

% This script is meant to be appended to by the script SpaceExplorer2App1
SpaceExplorer2App1;