%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%IMPORTANT NOTE: THIS PROGRAM TAKES ABOUT 3 MINUTES TO RUN
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Let us use a model for binding of the form:
%                   
%   The sum from 1 to v of C_i = v!/((v-i)!*i!)*K_x^(i-1))*(tnpbsa/kd_spec)*r*i,
%                       (See Stone et al.)
%
%v is the valency of the TNP-X-BSA, and we are going to find the value of
%v which yields the closest fit to Lux's data. kx is some positive value
%s.t. K_x = 10^kx, and the error function we will be using will fit a value
%of kx rather than a value of K_x. r is the expression level of a
%particular receptor in a cell, and kd_spec is the Kd value associated with
%the binding of the receptor with the pertinent flavor of immunoglobulin.
%
%In this program, we will be using Kd values derived exclusively from
%Bruhns et al.
%
%Finding receptor expression, kx, and v by means of minimizing an error 
%function. I have created the function Error for this purpose, which is used 
%to fit curves for both the TNP-4-BSA and TNP-26-BSA data (see Error.m).
%
%Per value of v from 1 to 10, we use the class GlobalSearch together with 
%fmincon to find the values of R, a six-dimensional vector, and kx, a seventh
%element appended to the six-dimensional vector R, which yield the minimum 
%value of Error per value of v. fmincon returns a 7-dimensional vector R, 
%the first six elements being the calculated expression levels of FcgRIA, 
%FcgRIIA-Arg, FcgRIIA-His, FcgRIIB, FcgRIIIA-Phe, and FcgRIIIA-Val and the 
%last element being a constant kx s.t. 10^kx = K_x yields the best fit to 
%the data using this model granted a particular valency v. The
%best fits for each value of v are saved and then compared to see which
%value of v yields the best fit to the data.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc; clear;

%Load the Kd values from Mimoto and Bruhns, the molarity of TNP-X-BSA used
%by Lux (see Figure 2), the normalized, background-MFI-adjusted MFIs from
%Lux, and the Kd values exclusively from Bruhns
[kd, tnpbsa, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 10
biCoefMat = zeros(10,10);
for k = 1:10
    for j = k:10
        biCoefMat(j,k) = nchoosek(k,j);
    end
end

%Set up parameters for GlobalSearch and fmincon
opts = optimoptions(@fmincon);
gs = GlobalSearch;
gs.StartPointsToRun = 'bounds-ineqs';
gs.Display = 'final';

%Begin optimization:
% > Rx is the vector R which yields the minimum value of Error for a
%   particular value of v.
% > Rc is a matrix whose ten columns are all values of Rx with their
%   corresponding value of v appended as eighth elements.
% > best is the column of Rc which yields the minimum value of Error.
% > best4 and best26 yield the minimum values of Error for the TNP-4-BSA
%   data and the TNP-26-BSA data, respectively.
for j = 1:2
    if j == 1
        mfiAdjMean = mfiAdjMean4;
    else
        mfiAdjMean = mfiAdjMean26;
    end
    for k = 1:10
        problem = createOptimProblem('fmincon','objective',...
        @(x) Error(x,kdBruhns,tnpbsa,mfiAdjMean,k,biCoefMat),'x0',ones(7,1),'lb',zeros(7,1),'ub',(100*ones(7,1)),'options',opts);
        Rx = run(gs,problem) %Not suppressed to allow for observation while running
        if k == 1
            Rc = [Rx; 1];
        else
            Rc = [Rc [Rx; k]];
        end
    end
    
    %Lists values of R which best fit the model for valency v for all
    %integers v from 1 to 10. The value of v is appended as an eighth
    %element of R. After running RegressionAndResiduals, type "Rc4" and
    %"Rc26" to view the best fits for all values of v for TNP-4-BSA and
    %TNP-26-BSA, respectively
    if j == 1
        Rc4 = Rc;
    else
        Rc26 = Rc;
    end
    
    %From all best fits from v = 1 to v = 10, find the value of v and its
    %corresponding vector R which yield the least summed squared error
    best = Rc(:,1);
    for k = 2:10
        if Error(best(1:7),kdBruhns,tnpbsa,mfiAdjMean,best(8),biCoefMat) > Error(Rc(1:7,k),kdBruhns,tnpbsa,mfiAdjMean,k,biCoefMat)
            best = Rc(:,k);
        end
    end
    
    %Type "best4" and "best26" to find the values of R (and, appended to R
    %as an eighth element, the valency v) which yield the least summed
    %squared errors for TNP-4-BSA and TNP-26-BSA, respectively
    if j == 1
        best4 = best;
    else
        best26 = best;
    end
end

%Calculate the expression levels per receptor flavor per valency for both
%TNP-4-BSA and TNP-26-BSA data
for j = 1:2
    if j == 1
        best = best4;
    else
        best = best26;
    end
    
    %The following matrix bestCoefMat is only made to pass into the
    %function Bound, and it passes information regarding the value of kx
    %which yields the best fit into the function (to see how this matrix is
    %used in the function Bound, please see its code)
    bestCoefMat = biCoefMat;
    for k = 1:10
        for l = 1:10
            bestCoefMat(k,l) = biCoefMat(k,l) * 10^(best(7)+k-1)*tnpbsa;
        end
    end
    
    %Results for MFI per flavor of receptor per flavor of immunoglobulin
    %that we would expect based on our optimization
    mfiExp = zeros(24,4);
    for k = 1:6
        for l = 1:4
            mfiExp((4*(k-1)+l),:) = ones(1,4)*Bound(best(k),kdBruhns(k,l),tnpbsa,best(8),bestCoefMat);
        end
    end
    
    if j == 1
        mfiExp4 = mfiExp;
    else
        mfiExp26 = mfiExp;
    end
end

%Calculate the residuals against the model for both the TNP-4-BSA data and
%the TNP-26-BSA data
mfiDiff4 = mfiExp4 - mfiAdjMean4;
mfiDiff26 = mfiExp26 - mfiAdjMean26;

%Lux's data and the model should yield that [best1 best2] equals:
%
%    [0.1050    0.0605
%     0.3415    0.4570
%     0.5322    0.5618
%     1.3456    1.9610
%     0.6046    0.7034
%     0.7153    0.6214
%     0.1294    0.1304
%     2.0000    2.0000]
%
%2.000 in each case being the best-fitting valency.

%Graphically display residuals:
bar3(mfiDiff4)
title('Residuals for TNP-4-BSA')
hold on
figure
bar3(mfiDiff26)
title('Residuals for TNP-26-BSA')