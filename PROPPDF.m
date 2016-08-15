function logprob = PROPPDF(x,y,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
    stdR,stdKx,stdc,stdsigma)
    %For logR
    logstdR = log(abs(stdR));
    logprob = 0;
    for j = 1:6
        CURRENT = y(j);
        logprob = logprob+logstdR-stdR*abs(x(j)-CURRENT);
        logprob = logprob-log((1-exppdf(CURRENT-lbR,stdR)))-...
            log(1-exppdf(ubR-CURRENT,stdR))+log(2);
    end
    %For logKx
    CURRENT = y(7);
    logprob = logprob+log(abs(stdKx))-stdKx*abs(x(7)-CURRENT);
    logprob = logprob-log(1-exppdf(CURRENT-lbKx,stdKx))-...
        log(1-exppdf(ubKx-CURRENT,stdKx))+log(2);
    %For logc
    logstdc = log(abs(stdc));
    for j = 8:9
        CURRENT = y(j);
        logprob = logprob+logstdc-stdc*abs(x(j)-CURRENT);
        logprob = logprob-log(1-exppdf(CURRENT-lbc,stdc))-...
            log(1-exppdf(ubc-CURRENT,stdc))+log(2);
    end
    %For v
    for j = 10:11
        CURRENT = y(j);
        if (CURRENT == lbv) || (CURRENT == ubv)
            logprob = logprob-log(2);
        else
            logprob = logprob-log(3);
        end
    end
%     For common logarithm of standard deviation coefficient
    CURRENT = y(12);
    logprob = logprob+log(abs(stdsigma))-stdsigma*abs(x(12)-CURRENT);
    logprob = logprob-log(1-exppdf(CURRENT-lbsigma,stdsigma))-...
        log(1-exppdf(ubsigma-CURRENT,stdsigma))+log(2);
end