function J = Error( R )

%This function requires the matrices stored in mfiAdjMean.mat and
%boundExp.mat to function. To make these accessible to the fuction Error
%without creating any new .mat files, I had to write them into this file.
%If you are already aware of the derivation of mfiAdjMean and boundExp,
%please skip through the file until you reach the creation of the vector
%"error"

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
    %immune complexes per flavor of receptor per flavor of immunoglobulin
    %should be as follows:
    boundExp = zeros(6,4);
    for j = 1:6
        for k = 1:4
            boundExp(j,k) = tnpbsa / (tnpbsa + kd(j,k));
        end
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    error = zeros(1,192);
    
    for j = 1:6
        for k = 1:4
            for l = 1:8
                error(32*(j-1) + 8*(k-1) + l) = (R(j)*boundExp(j,k) - mfiAdjMean((4*(j-1)+k),l))^2;
            end
        end
    end
    J = nansum(error);
end