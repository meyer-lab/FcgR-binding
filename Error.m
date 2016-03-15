function J = Error( R )

%This function requires the matrices stored in mfiAdjMean.mat and
%boundExp.mat to function. To make these accessible to the fuction Error
%without creating any new .mat files, I had to write them into this file.
%If you are already aware of the derivation of mfiAdjMean and boundExp,
%please skip through the file until you reach the creation of the vector
%"error"

    [mfiAdjMean, kd] = loadData();

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
    error = zeros(size(mfiAdjMean));
    
    for j = 1:6
        for k = 1:4
            error(4*(j-1)+k,:) = (R(j)*boundExp(j,k) - mfiAdjMean(4*(j-1)+k,:)).^2;
        end
    end
    J = nansum(nansum(error));
end