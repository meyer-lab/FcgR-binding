function [J, mfiExpPre] = Error3( Rtot, kd, mfiAdjMean, v, biCoefMat,opts)
    Rtot = 10.^Rtot;
    
    L = Rtot(8);
    kx = Rtot(7);

    Req = zeros(6,4);
    z = [10, 1, 0.1, 0.01, 0.001, 0.0001];
    for j = 1:6
        for k = 1:4
            troll = Req(j,k);
            for l = 1:size(z,2);
                x = z(l);
                while troll*(1+v*L/kd(j,k)*(1+kx*troll)^(v-1)) < Rtot(j)
                    troll = troll+x;
                end
                troll = troll - x;
            end
            Req(j,k) = troll;
        end
    end
    
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
            for l = 1:length(CoefVec)
                mfiExpPre(j,k) = mfiExpPre(j,k)+CoefVec(l)*Req(j,k)^l;
            end
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