x = normrnd(0,1,1,1000);
y = 5*x;
for j = 1:10
    std(y)
    pause(0.2)
end

run temp