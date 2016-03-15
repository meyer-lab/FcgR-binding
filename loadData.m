function [mfiAdjMean, kd] = loadData ()
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
end