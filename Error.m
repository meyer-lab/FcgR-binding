function [J, mfiExp] = Error( Rtot, kd, mfiAdjMean4, mfiAdjMean26, v, biCoefMat,tnpbsa)
    Rtot = 10.^Rtot;
    kx = Rtot(7);
    L = tnpbsa;
    
    Req4 = zeros(6,4);
    Req26 = zeros(6,4);
    
    ReqFunc = @(Reqi, R, kdi, Li) R - Reqi*(1+v*Li/kdi*(1+kx*Reqi)^(v-1));
    
    for j = 1:6
        for k = 1:4
            Req4(j,k) = fzero(@(x) ReqFunc(10^x,Rtot(j),kd(j,k),L(1)), -1);
            Req26(j,k) = fzero(@(x) ReqFunc(10^x,Rtot(j),kd(j,k),L(2)), -1);
        end
    end
    
    Req4 = 10.^Req4;
    Req26 = 10.^Req26;
    
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
    mfiExpPre4 = zeros(6,4);
    mfiExpPre26 = zeros(6,4);
    for j = 1:6
        for k = 1:4
            mfiExpPre4(j,k) = nansum(CoefVec.*Req4(j,k).^(1:v)');
            mfiExpPre26(j,k) = nansum(CoefVec.*Req26(j,k).^(1:v)');
        end
    end
    mfiExpPre4 = mfiExpPre4./kd;
    mfiExpPre26 = mfiExpPre26./kd;
        
    mfiExp4 = zeros(24,4);
    mfiExp26 = zeros(24,4);
    for j = 1:6
        for k = 1:4
            mfiExp4((4*(j-1)+k),:) = mfiExpPre4(j,k)*ones(1,4);
            mfiExp26((4*(j-1)+k),:) = mfiExpPre26(j,k)*ones(1,4);
        end
    end
    mfiExp = [mfiExp4, mfiExp26];
    
    J = nansum(nansum([(mfiExp4 - mfiAdjMean4).^2, (mfiExp26 - mfiAdjMean26).^2]));
end