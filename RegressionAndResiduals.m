clc; clear;

%Load the mean fluorecent intensities provided by Lux's lab and affinities
[mfiAdjMean, kd, tnpbsa, boundExp] = loadData();

%Finding receptor expression by means of minimizing an error function. The
%error function we desire is too complex to write in as an anonymous
%function in MATLAB; therefore, I wrote it in the file Error.m. We use the 
%MATLAB function fmincon to find the value of R, a six-dimensional vector, 
%which yields the minimum value of Error

optFun = @(x) Error(x, mfiAdjMean, boundExp);

R = fmincon(optFun,ones(6,1),[],[],[],[],zeros(6,1),(1e6*ones(6,1)));

%R is approximately equal to:
%
%   [1.5278 ; 12.9234 ; 15.9374 ; 35.4406 ; 9.6195 ; 1.7717]
%
%R(1) is the estimate of the expression level for FcgRIA, R(2) the estimate
%of the expression level of FcgRIIA-Arg, etc. conflated with the coversion
%factor from MFI to quantity of receptors

%Using this estimate R, the MFI we would expect per flavor of receptor per
%flavor of immunoglobulin per replicate (mfiExp) is as follows:

[~, bndCalc]  = optFun( R );

%Therefore, the the difference in mfiExp and mfiAdj is as follows; let this
%matrix be called mfiDiff:

mfiDiff = bndCalc - mfiAdjMean;
mfiDiff(:,5:end) = [];

%Saving this matrix as a .csv file
%csvwrite('MFIResiduals.csv',mfiDiff)

%See a bar graph of the elements of mfiDiff against their indices:

%bar(mfiDiff)
%title('Residuals of MFI from Luxs Data Against Our Model')


%%%%%% Aaron diagnosis


kdV = reshape(kd,1,[]);







