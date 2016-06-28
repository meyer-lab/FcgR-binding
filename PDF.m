function [logprob] = PDF(x, kd, mfiAdjMean, biCoefMat, tnpbsa, meanPerCond, stdPerCond)
    %Find residuals for the model granted current parameters
    
    %mfiExpPre is a 6x8 matrix which includes the predicted value by the
    %given parameter fit for each combination of FcgR, IgG, and valency. It
    %is the concatenation of matrices mfiExpPre4 and mfiExpPre26; see
    %Error.m for their definiton
    [~,~,mfiExpPre] = ErrorAvidityChange(x',kd,mfiAdjMean,biCoefMat,tnpbsa);
    
    %Check to see that for the parameter fit there exist expected values
    %for the data (see Error.m lines 23 through 28)
    if mfiExpPre(1,1) == -1 || max(x) > 8
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
                 logprob = logprob + pseudoNormlike(mfiExpPre(j,4*(l-1)+k), ...
                     meanPerCond(4*(j-1)+k,l),stdPerCond(4*(j-1)+k,l));
            end
        end
    end
end
%--------------------------------------------------------------------------
function logprob = pseudoNormlike(x,mu,sigma)
    %To replace normlike in the function PDF; while normlike returns
    %negated log probabilities, this function returns log probabilities as
    %they are.
    z = (x - mu) / sigma;
    logprob = -.5 * z^2 - log(sqrt(2.*pi).*sigma);
end