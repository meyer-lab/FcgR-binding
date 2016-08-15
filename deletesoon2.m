function [logparam] = deletesoon2(logKda, logKdb, v, logKx,...
    logL, logR,whichArg)

    [La,Rmultia] = StoneAlt(logKda, v, logKx, logL, logR);
    [Lb,Rmultib] = StoneAlt(logKdb, v, logKx, logL, logR);
    
    logLrat = log10(La/Lb);
    logRmultirat = log10(Rmultia/Rmultib);
    
    if whichArg == 'L'
        logparam = logLrat;
    else
        logparam = logRmultirat;
    end
end