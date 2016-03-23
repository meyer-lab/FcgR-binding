function [J] = Error( R, kd, tnpbsa, mfiAdjMean, v )

%   R is a seven-dimensional vector whose first six elements are
%   expression levels of FcgRIA, FcgRIIA-Arg, etc. and whose seventh
%   element is kx (see RegressionAndResiduals.m). kd is a 6 X 4
%   matrix whose elements represent the Kd values associated with each
%   flavor of immunoglobulin per flavor of receptor. tnpbsa is derived in
%   loadData.m, as is mfiAdjMean; v is the valency of the TNP-X-BSA.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    temp1 = zeros(1,96);
    for j = 1:6
        for k = 1:4
            temp2 = Bound(R(j),R(7),kd(j,k),tnpbsa,v);
            temp1((16*(j-1)+4*(k-1)+1):(16*(j-1)+4*(k-1)+4)) = temp2*ones(1,4);
        end
    end
    
    error = zeros(1,96);
    temp3 = mfiAdjMean';
    for j = 1:96
        error(j) = (temp1(j) - temp3(j))^2;
    end
    
    J = nansum(error);
end