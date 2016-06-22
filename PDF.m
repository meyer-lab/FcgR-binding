function [logprob] = PDF(x, kd, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa, meanPerCond, stdPerCond)
    %Find residuals for the model granted current parameters
    
    %mfiExpPre is a 6x8 matrix which includes the predicted value by the
    %given parameter fit for each combination of FcgR, IgG, and valency. It
    %is the concatenation of matrices mfiExpPre4 and mfiExpPre26; see
    %Error.m for their definiton
    [~,~,mfiExpPre] = Error(x',kd,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa);

    
    %Check to see that for the parameter fit there exist expected values
    %for the data (see Error.m lines 23 through 28)
    if isempty(mfiExpPre) || max(x) > 8
        logprob = -Inf;
        return
    end
    
    %Create a matrix which includes the log probability of the model being
    %chosen for each combination of data from one FcgR, one IgG, and one
    %valency
    logprob = 0;
    for j = 1:6
        for k = 1:4
            for l = 1:2
                 logprob = logprob + log(normpdf(mfiExpPre(j,4*(l-1)+k), ...
                     meanPerCond(4*(j-1)+k,l), stdPerCond(4*(j-1)+k,l)));
            end
        end
    end
end