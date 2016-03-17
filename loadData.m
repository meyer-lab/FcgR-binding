function [kd, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData ()
    mfi = csvread('Luxetal2013-Fig2B.csv',2,2);
    mfi(29,1) = nan;

    
    
    %Load the Kd values we found in the literature
    kd = csvread('FcR-Kd.csv',1,1);

    %Create a matrix of MFIs per receptor flavor per immunoglobulin flavor per
    %replicate minus background MFI per flavor of immunoglobulin flavor per
    %replicate
    mfiAdj = zeros(size(mfi));
    for j = 1:8
        mfiAdj(:,j) = mfi(:,j) - mean(mfi(1:5:end,j));
    end
    mfiAdj(1:5:end,:) = [];

    %Normalize the adjusted MFIs along the replicates (along the columns)
    mfiAdjMean = zeros(24,8);
    for j = 1:8
        mfiAdjMean(:,j) = mfiAdj(:,j) / nanmean(mfiAdj(:,j));
    end    
    
    %Separate the MFIs from TNP-4-BSA trials from those from TNP-26-BSA
    %trials
    mfiAdjMean4 = mfiAdjMean(:,1:4);
    mfiAdjMean26 = mfiAdjMean(:,5:8);
    
    %Load the Kd values found exclusively from Bruhns et al. (2009)
    kdBruhns = csvread('FcR-Kd-2.csv');
    
end