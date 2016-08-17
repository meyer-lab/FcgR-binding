function [samppostburnin, burninmax] = gewekestrain(sample, stringency)
    len = size(sample,1);
    dim = size(sample,2);
    dimsqr = dim^2;
    if len < 300
        error(['The function geweke can only handle samples of at least' ...
            '300 in size.'])
    end
    burninmax = 1;
    scores = geweke(sample(burninmax:len,:));
    tests = normpdf(scores);
    for j = 1:dimsqr
        if tests(j) > 0.5
            tests(j) = 1-tests(j);
        end
    end
    fail = (tests < stringency);
    if sum(sum(fail)) > 0
        error(['The sampler did not have long enough of a burn-in period;' char(10)...
            'it did not run long enough for the last 300 samples to have '...
            'reached' char(10) 'ergodicity. The number of samples used, evidently, was '...
            num2str(len) ' samples.'])
    end
    burnin = ceil(burninmax/2);
    while 1
        if burninmax == burnin
            burnin = burninmax-1;
            if burnin == 0
                samppostburnin = sample(burninmax:len,:);
                return
            end
        end
        if burninmax-burnin == 1
            scores = geweke(sample(burnin:len,:));
            tests = normpdf(scores);
            for j = 1:dimsqr
                if tests(j) > 0.5
                    tests(j) = 1-tests(j);
                end
            end
            fail = (tests < stringency);
            if sum(sum(fail)) == 0
                burninmax = burnin;
            end
            samppostburnin = sample(burninmax:len,:);
            return
        end
        scores = geweke(sample(burnin:len,:));
        tests = normpdf(scores);
        for j = 1:dimsqr
            if tests(j) > 0.5
                tests(j) = 1-tests(j);
            end
        end
        if sum(sum(tests)) > 0
            burnin = ceil(burnin+(burninmax-burnin)/2);
        else
            burninmax = burnin;
            burnin = ceil(burninmax/2);
        end
    end
end