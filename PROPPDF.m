function [prob] = PROPPDF(x, y, kdBruhns, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa, minAICc)
%     temp = zeros(1,7);
%     for j = 1:7
%         temp(j) = normpdf(x(j),y(j),0.2);
%     end
%     prob = prod(temp);

    temp = zeros(1,7);
    for j = 1:7
        temp(j) = unifpdf(x(j)-y(j),-0.2,0.2);
    end
    prob = prod(temp);
end