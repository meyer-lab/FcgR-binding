clear;clc;close all;

len = 10000;
dim = 10;
dimsqr = dim^2;
stringency = [0.05 0.08 0.1];

plotter = zeros(len-300,3);

sample = randn(len,dim);
for j = 1:(len-300)
    for k = 1:3
        strin = stringency(k);
        scores = geweke(sample(j:len,:));
        tests = normpdf(scores);
        for l = 1:dimsqr
            if tests(l) > 0.5
                tests(l) = 1-tests(l);
            end
            fail = (tests < strin);
            if sum(sum(fail)) > 0
                plotter(j,k) = 1;
            end
        end
    end
    clc
    disp(j/(len-300));
end

plot(plotter)