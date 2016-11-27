function [kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData()
    %Clear workspace and command window
    clear; clc;

    mfi = csvread('Luxetal2013-Fig2B.csv',2,2);
    mfi(29,1) = nan;

    %Create a figure for the molarity of TNP-X-BSA in the solution into which 
    %the CHO cells were placed (see Lux et al. 2013, Figure 2). The molecular
    %weight of bovine serum albumin is 66430 Da, and the molecular weight of 
    %a TNP group is about 212 Da. The contration of TNP-X-BSA in the solution 
    %described in Figure 2 is 5 micrograms per milliliter. Molecular
    %weights found from source cited in the paper in Overleaf.
    tnpbsa4 = 1/67122 * 1e-3 * 5;
    tnpbsa26 = 1/70928 * 1e-3 * 5;
    tnpbsa = [tnpbsa4;tnpbsa26];
    
    %Load the Kd values we found in the literature
    kd = csvread('FcR-Kd-2.csv',1,1);

    %Create a matrix of MFIs per receptor flavor per immunoglobulin flavor per
    %replicate minus background MFI per flavor of immunoglobulin flavor per
    %replicate
    mfiAdj = zeros(size(mfi));

    for j = 1:6
        for k = 1:8
            mfiAdj(5*(j-1)+2:5*j,k) = mfi(5*(j-1)+2:5*j,k) - mfi(5*(j-1)+1,k);
        end
    end
    mfiAdj(1:5:end,:) = [];

    %Normalize the adjusted MFIs along each replicate
    mfiAdjMean = zeros(24,8);
    for j = 1:4
        mfiAdjMean(:,j) = mfiAdj(:,j) / nanmean([mfiAdj(:,j); mfiAdj(:,j+4)]);
        mfiAdjMean(:,j+4) = mfiAdj(:,j+4) / nanmean([mfiAdj(:,j); mfiAdj(:,j+4)]);
    end
    
    %Load the Kd values found exclusively from Bruhns et al. (2009)
    kdBruhns = csvread('FcR-Kd-2.csv');
    
    %Load the point which yields the best fit
%     load('best.mat')
    best = ones(1,13);
    
    %From mfiAdjMean, create matrices which hold the adjusted expression
    %level mean and expression level standard deviation for each condition
    %(i.e. FcgR with IgG1, valency 4)
    meanPerCond = zeros(24,2);
    stdPerCond = zeros(24,2);
    for j = 1:24
        for k = 1:2
            meanPerCond(j,k) = nanmean(mfiAdjMean(j,4*(k-1)+1:4*k));
            stdPerCond(j,k) = std(mfiAdjMean(j,4*(k-1)+1:4*k),0,2,'omitnan');
        end
    end
    
end