function [J, mfiExp] = Error( Rtot, kd, mfiAdjMean, v, biCoefMat)
    Rtot = 10.^Rtot;
    kx = Rtot(7);
    L = Rtot(8);
    
    Req = zeros(6,4);
    
    ReqFunc = @(Reqi, R, kdi) R - Reqi*(1+v*L/kdi*(1+kx*Reqi)^(v-1));
    
    for j = 1:6
        for k = 1:4
            Req(j,k) = fzero(@(x) ReqFunc(10^x,Rtot(j),kd(j,k)), -1);
        end
    end
    
    Req = 10.^Req;
    
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
    
    CoefVec = biCoefMat(1:v,v) .* Rtot(size(Rtot,1)-1).^((1:v)'-1)*Rtot(size(Rtot,1));
    mfiExpPre = zeros(6,4);
    for j = 1:6
        for k = 1:4
            mfiExpPre(j,k) = nansum(CoefVec.*Req(j,k).^(1:v)');
        end
    end
    mfiExpPre = mfiExpPre./kd;
        
    mfiExp = zeros(24,4);
    for j = 1:6
        for k = 1:4
            mfiExp((4*(j-1)+k),:) = mfiExpPre(j,k)*ones(1,4);
        end
    end
    
    J = nansum(nansum((mfiExp - mfiAdjMean).^2));
end