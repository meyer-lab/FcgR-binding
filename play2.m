function covariance = play2(A)
    n = length(A);
    m = size(A,2);
    covariance = zeros(size(A,2));
    
    for j = 1:m
        for k = 1:m
            x = A(:,j);
            y = A(:,k);
            
            meanx = mean(x);
            meany = mean(y);
            a = x - meanx;
            b = y - meany;
            covariance(j,k) = (a'*b)/n;
        end
    end
end