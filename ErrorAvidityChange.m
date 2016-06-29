function [J, mfiExp, mfiExpPre, mfiDiff] = ErrorAvidityChange(RtotTrue, Kd,...
    mfiAdjMean, biCoefMat, tnpbsa)
    %Treats the last two elements of RtotTrue as the effective avidities of
    %TNP-4-BSA and TNP-26-BSA respectively (as of June 27, 2016, these are
    %elements 10 and 11). Runs Error.m inputting these two avidities as a
    %two-dimensional column vector which is passed into Error as the vector
    %v.
    
    % If error is called with Rtot being a single value, assume we want to
    % have constant expression across all the receptors
    if numel(RtotTrue) == 6
        RtotTrue = [RtotTrue(1) * ones(6,1); RtotTrue(2:6)];
    end
    
    [J, mfiExp, mfiExpPre] = Error(RtotTrue(1:9),Kd,mfiAdjMean,ceil(RtotTrue(10:11)),...
        biCoefMat,tnpbsa);
    
    mfiDiff = mfiExp - mfiAdjMean;
end