clear;clc;

% Initialize persistent variables in NormalErrorCnct
NormalErrorCnct;

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
Riss = lbR:(ubR-lbR)/2:ubR;
Kxiss = lbKx:(ubKx-lbKx)/2:ubKx;
viss = 1:29/3:30;
viss = ceil(viss);

RissL = length(Riss);
vissL = length(viss);

%Set up cell arrays of tentative global optima and their log-likelihoods
ptent = cell(RissL-1,RissL-1,RissL-1,RissL-1,RissL-1,RissL-1,RissL-1,...
    vissL-1,vissL-1);
lntent = ptent;

% Set up options for genetic algorithm
options = gaoptimset('display','off');

% Iterate over each parameter range and find global optimum
for j = 1:(RissL-1)
    lbR1 = Riss(j);
    ubR1 = Riss(j+1);
    for k = 1:(RissL-1)
        lbR2 = Riss(k);
        ubR2 = Riss(k+1);
        for l = 1:(RissL-1)
            lbR3 = Riss(l);
            ubR3 = Riss(l+1);
            for m = 1:(RissL-1)
                lbR4 = Riss(m);
                ubR4 = Riss(m+1);
                for n = 1:(RissL-1)
                    lbR5 = Riss(n);
                    ubR5 = Riss(n+1);
                    for o = 1:(RissL-1)
                        lbR6 = Riss(o);
                        ubR6 = Riss(o+1);
                        for p = 1:(RissL-1)
                            lbKx = Riss(p);
                            ubKx = Riss(p+1);
                            for q = 1:(vissL-1)
                                lbv1 = viss(q);
                                ubv1 = viss(q+1);
                                for r = 1:(vissL-1)
                                    lbv2 = viss(r);
                                    ubv2 = viss(r+1);
                                    
                                    [x,fval] = ga(@(x) -NormalErrorCnct(x),...
                                        12,[],[],[],[],[lbR1 lbR2 lbR3 lbR4...
                                        lbR5 lbR6 lbKx lbc lbc lbv1 lbv2...
                                        lbsigma],[ubR1 ubR2 ubR3 ubR4 ubR5...
                                        ubR6 ubKx ubc ubc ubv1 ubv2 ubsigma],...
                                        [],[11 12], options);
                                    ptent{j,k,l,m,n,o,p,q,r} = x;
                                    lntent{j,k,l,m,n,o,p,q,r} = -fval;
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end

save('SpaceExplorerData.mat','RissL','vissL','ptent','lntent')
% This script is meant to be appended to by the script SpaceExplorerApp1
SpaceExplorerApp1;