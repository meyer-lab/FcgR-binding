function loglike = normlikeTEMP(x,mu,sigma)
    loglike = -normlike([mu sigma],x);
end