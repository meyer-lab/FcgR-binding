function [output] = proprnd(x)
%     test = 0;
%     while test == 0
%         temp = x.^10 + normrnd(0,0.5,1,7);
%         test = prod((0 < temp) .* (temp < 10));
%     end
%     output = log10(temp);

%     output = log10(mod(10.^x + normrnd(0,0.1,1,7),10));
    output = x + normrnd(0,0.2,1,7);
end