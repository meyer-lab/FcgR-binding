function [J, mfiExp] = Error( Rtot, kd, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa)
    Rtot = 10.^Rtot;
    kx = Rtot(2);
    L = tnpbsa;
    
    %Preallocating space for the Req values (according to Stone et al.) for
    %each combination of IgG and FcgR per flavor of TNP-X-BSA.
    Req4 = zeros(6,4);
    Req26 = zeros(6,4);
    
    ReqFunc = @(Reqi, R, kdi, Li, vi) R - Reqi*(1+vi*Li/kdi*(1+kx*Reqi)^(vi-1));
    
    %Finding Req values by means of bisection algorithm
    for j = 1:6
        for k = 1:4
            Req4(j,k) = bisection(@(x) ReqFunc(10^x,Rtot(j),kd(j,k),L(1),v(1)),-5,5,1e-10);
            Req26(j,k) = bisection(@(x) ReqFunc(10^x,Rtot(j),kd(j,k),L(2),v(2)),-5,5,1e-10);
            if isnan(Req4(j,k))
                Req4(j,k) = -Inf;
            end
            if isnan(Req26(j,k))
                Req26(j,k) = -Inf;
            end
        end
    end
    %Preventing errors in global optimization due to failure of the
    %above local solver
    if max(max(isnan(Req4))) || max(max(isnan(Req26)))
        J = 1E6;
        mfiExp = [];
        return;
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
    %for all i from 1 to v for all v from 1 to 10
    
    CoefVec4 = biCoefMat(1:v(1),v(1)) .* Rtot(size(Rtot,1)).^((1:v(1))'-1)*L(1);
    CoefVec26 = biCoefMat(1:v(2),v(2)) .* Rtot(size(Rtot,1)).^((1:v(2))'-1)*L(2);
    
    %Creating matrix of expected MFIs; takes a few steps to do so
    mfiExpPre4 = zeros(6,4);
    mfiExpPre26 = zeros(6,4);
    for j = 1:6
        for k = 1:4
            mfiExpPre4(j,k) = nansum(CoefVec4.*Req4(j,k).^(1:v(1))');
            mfiExpPre26(j,k) = nansum(CoefVec26.*Req26(j,k).^(1:v(2))');
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
    %Expected MFIs
    mfiExp = [mfiExp4, mfiExp26];
    
    %Error
    J = nansum(nansum([(mfiExp4 - mfiAdjMean4).^2, (mfiExp26 - mfiAdjMean26).^2]));
end