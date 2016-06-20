%0 to 10 in 2D

x = [0:0.01:1000];
prob = zeros(1001,1001);
for j = 1:1001
    for k = 1:1001
        prob(j,k) = normpdf(x(j),5,2)*normpdf(x(k),5,2);
    end
end

plot(x,x,prob)
figure

