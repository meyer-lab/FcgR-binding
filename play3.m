n = 500000;
x = zeros(n,1);
x(1) = 0.5;
for i = 1:n-1
    x_c = normrnd(x(i),0.05);
    if rand < min(1,normpdf(x_c)/normpdf(x(i)))
        x(i+1) = x_c;
    else
        x(i+1) = x(i);
    end
end

hist(x,100)