function [J, mfiExp, mfiExpPre] = Error(Rtot, Kd, mfiAdjMean, v, biCoefMat, tnpbsa)
    % If error is called with Rtot being a single value, assume we want to
    % have constant expression across all the receptors
    if numel(Rtot) == 4
        Rtot = [Rtot(1) * ones(6,1); Rtot(2:4)];
    end
    %Convert from log scale
    Rtot = 10.^Rtot;
    Kx = Rtot(7);
    
    %Get expected value of MFIs (before conversion factors) from Equation 7
    %from Stone
    mfiExpPrePre = zeros(6,8);
    for j = 1:6
        for k = 1:4
            mfiExpPrePre(j,k) = StoneSolver(Rtot(j),Kx,v(1),Kd(j,k), ...
                tnpbsa(1),biCoefMat);
            mfiExpPrePre(j,k+4) = StoneSolver(Rtot(j),Kx,v(2),Kd(j,k), ...
                tnpbsa(2),biCoefMat);
        end
    end
    
    %Multiply by conversion factors
    mfiExpPre = Rtot(8)*mfiExpPrePre;
    mfiExpPre(:,5:8) = Rtot(9)*mfiExpPrePre(:,5:8);
    
    %Check for undefined values (errors from ReqFuncSolver)
    if max(max(mfiExpPre == -1))
        J = 1e8;
        mfiExpPre = -ones(6,8);
        mfiExp = -ones(6,8);
        return
    end
    
    %Create array of expected values to calculate residuals
    mfiExp = zeros(24,8);
    for j = 1:6
        for k = 1:4
            mfiExp((4*(j-1)+k),1:4) = mfiExpPre(j,k)*ones(1,4);
            mfiExp((4*(j-1)+k),5:8) = mfiExpPre(j,k+4)*ones(1,4);
        end
    end
    
    %Error
    J = nansum(nansum((mfiExp-mfiAdjMean).^2));
end