%Load the mean fluorecent intensities provided by Lux's lab
load mfi.mat

%Load the Kd values we found in the literature
load kd.mat

%Create a matrix of MFIs per receptor flavor per immunoglobulin flavor per
%replicate minus background MFI per flavor of immunoglobulin flavor per
%replicate
mfiAdj = zeros(24,8);
for j = 1:6
    for k= 1:4
        mfiAdj((4*(j-1)+k),:) = mfi((5*j-4+k),:) - mfi((5*j-4),:);
    end
end

%Normalize the adjusted MFIs along the replicates (along the columns)
mfiAdjMean = zeros(24,8);
temp = nanmean(mfiAdj);
for j = 1:8
    mfiAdjMean(:,j) = mfiAdj(:,j) / temp(j);
end

%Create a figure for the molarity of TNP-X-BSA in the solution into which 
%the CHO cells were placed (see Lux et al. 2013, Figure 2). The molecular
%weight of bovine serum albumin is 66463 Da, and the contration of
%TNP-X-BSA in the solution described in Figure 2 is 5 micrograms per
%milliliter
tnpbsa = 1/66463 * 1e-6 * 5 * 1e3;

%Using a highly simplified model of receptor binding of the form
%                   
%                     C = R*L_0/(L_0 + K_D),
%
%granted the Kd values we have compiled, the expected number of bound
%immune complexes per receptor for each flavor of receptor for each flavor 
%of immunoglobulin should be as follows:
boundExp = zeros(6,4);
for j = 1:6
    for k = 1:4
        boundExp(j,k) = tnpbsa / (tnpbsa + kd(j,k));
    end
end

%Finding receptor expression by means of minimizing an error function. The
%error function we desire is too complex to write in as an anonymous
%function in MATLAB; therefore, I wrote it in the file Error.m. We use the 
%MATLAB function fmincon to find the value of R, a six-dimensional vector, 
%which yields the minimum value of Error

R = fmincon(@(x) Error(x),ones(6,1),[],[],[],[],zeros(6,1),(1e6*ones(6,1)))

%Saving R for use in later weeks:

save R

%R is approximately equal to:
%
%   [1.5278 ; 12.9234 ; 15.9374 ; 35.4406 ; 9.6195 ; 1.7717]
%
%R(1) is the estimate of the expression level for FcgRIA, R(2) the estimate
%of the expression level of FcgRIIA-Arg, etc. conflated with the coversion
%factor from MFI to quantity of receptors

%Using this estimate R, the MFI we would expect per flavor of receptor per
%flavor of immunoglobulin per replicate (mfiExp) is as follows:

temp = zeros(6,4);
for j = 1:6
    for k = 1:4
        temp(j,k) = R(j) * boundExp(j,k);
    end
end
temp2 = reshape(temp',24,1);
mfiExp = [temp2 temp2 temp2 temp2 temp2 temp2 temp2 temp2];

%Therefore, the the difference in mfiExp and mfiAdj is as follows; let this
%matrix be called mfiDiff:

mfiDiff = mfiExp - mfiAdjMean;

%Saving this matrix as a .csv file
xlswrite('MFIResiduals.csv',mfiDiff)

%See a bar graph of the elements of mfiDiff against their indices:

bar3(mfiDiff)
title('Residuals of MFI from Luxs Data Against Our Model')