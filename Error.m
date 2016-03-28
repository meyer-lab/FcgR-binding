function [J] = Error( R, kd, tnpbsa, mfiAdjMean, v )

%   R is a seven-dimensional vector whose first six elements are
%   expression levels of FcgRIA, FcgRIIA-Arg, etc. and whose seventh
%   element is kx (see RegressionAndResiduals.m). kd is a 6 X 4
%   matrix whose elements represent the Kd values associated with each
%   flavor of immunoglobulin per flavor of receptor. tnpbsa is derived in
%   loadData.m, as is mfiAdjMean; v is the valency of the TNP-X-BSA.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    temp1 = zeros(1,24);
    for j = 1:6
        for k = 1:4
            temp1(4*(j-1)+k) = Bound(R(j),R(7),kd(j,k),tnpbsa,v);
        end
    end
    temp2 = [temp1;temp1;temp1;temp1]';
    error = (temp2 - mfiAdjMean).^2;
        
    J = nansum(nansum(error));
end