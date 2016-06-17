function [prob] = PROPPDF(x, y, kdBruhns, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa, minAICc)
    temp = zeros(1,7);
    for j = 1:7
        temp(j) = normpdf(10^x(j),10^y(j),1);
    end
    prob = prod(temp);
end