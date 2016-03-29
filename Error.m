function [J, mfiExp] = Error( R, kd, tnpbsa, mfiAdjMean, v, biCoefMat )
    R = 10.^R;
    
%   R is a seven-dimensional vector whose first six elements are
%   expression levels of FcgRIA, FcgRIIA-Arg, etc. and whose seventh
%   element is kx (see RegressionAndResiduals.m). kd is a 6 X 4
%   matrix whose elements represent the Kd values associated with each
%   flavor of immunoglobulin per flavor of receptor. tnpbsa is derived in
%   loadData.m, as is mfiAdjMean; v is the valency of the TNP-X-BSA.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %Create a matrix of coefficients of the form:
    %v!/((v-i)!*i!)*10^(kx+i-1)*tnpbsa
    %for all i from 1 to v for all v from 1 to 10, using the value of kx at
    %which the model outputs a minimum error
    CoefMat = biCoefMat(1:v,v) .* (R(7).^((1:v)'-1))*tnpbsa;

    %Sum up squared errors
    mfiExp = zeros(24,4);
    for j = 1:6
        rKdVec = ((R(j).^(1:v))*CoefMat)';
        
        for k = 1:4  
            %Granted a receptor expression level r, the specific Kd
            %value of the pertinent receptor-immunoglobulin combination kd_spec,
            %the molarity of TNP-X-BSA used by Lux et al. (see Figure 2), valency v,
            %and a coefficient of the form:
            %v!/((v-i)!*i!)*10^(kx+i-1)*tnpbsa (many such coefficients being
            %contained in the matrix CoefMat), the number of immune complexes bound
            %to a cell should be as follows, according to the model from Stone et al.:
            %
            %   The sum from 1 to v of C_i = v!/((v-i)!*i!)*10^(kx*(i-1))*(tnpbsa/kd_spec)*r^i
            
            mfiExp(4*(j-1)+k,1:4) = rKdVec/kd(j,k);
        end
    end
        
    J = nansum(nansum((mfiExp - mfiAdjMean).^2));
end