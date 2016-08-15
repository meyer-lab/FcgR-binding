function sqrErr = tempforstd(x,best,tnpbsa,...
    mfiAdjMean,kdBruhns,meanPerCond,stdPerCond,biCoefMat,lbR,ubR,...
    lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,nsamples)

    stdR = x(1);
    stdKx = x(2);
    stdc = x(3);
    stdsigma = x(4);

    proppdf = @(x,y) PROPPDF(x,y,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
        stdR,stdKx,stdc,stdsigma);
    %Pseudo-random generator of new points to test; 0.039 gives accept of about
    %0.23 for 7 parameters
    proprnd = @(x) PROPRND_mex(x,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
        stdR,stdKx,stdc,stdsigma);
    %Probability distribution of interest
    pdf = @(x) NormalError_mex(x,kdBruhns,mfiAdjMean,tnpbsa,meanPerCond,...
        biCoefMat);
    
    %Run Metropolis-Hastings algorithm
    [~,accept] = mhsample(best,nsamples,'logpdf',pdf,'logproppdf',proppdf, ...
        'proprnd',proprnd,'symmetric',0,'burnin',0);
    
    sqrErr = (accept-0.23)^2;
end