<<<<<<< HEAD
function [kd, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData ()
=======
function [mfiAdjMean, kd, tnpbsa, boundExp] = loadData ()
>>>>>>> 15975d1ad7ef19e4b174dacac2ab1a51e6548b92
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
<<<<<<< HEAD
    end    
    
    %Separate the MFIs from TNP-4-BSA trials from those from TNP-26-BSA
    %trials
    mfiAdjMean4 = mfiAdjMean(:,1:4);
    mfiAdjMean26 = mfiAdjMean(:,5:8);
    
    %Load the Kd values found exclusively from Bruhns et al. (2009)
    kdBruhns = csvread('FcR-Kd-2.csv');
    
=======
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
>>>>>>> 15975d1ad7ef19e4b174dacac2ab1a51e6548b92
end