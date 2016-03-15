function [J, bndCalc, error]  = Error(R, mfiAdjMean, boundExp)

%This function requires the matrices stored in mfiAdjMean.mat and
%boundExp.mat to function. To make these accessible to the fuction Error
%without creating any new .mat files, I had to write them into this file.
%If you are already aware of the derivation of mfiAdjMean and boundExp,
%please skip through the file until you reach the creation of the vector
%"error"
    bndCalc = zeros(size(mfiAdjMean));
    
    for j = 1:6
        for k = 1:4
            bndCalc(4*(j-1)+k,:) = R(j)*boundExp(j,k);
        end
    end
    
    % Only calculating error for TNP-4-BSA
    error = (bndCalc(:,1:4) - mfiAdjMean(:,1:4)).^2;
    J = nansum(nansum(error));
end