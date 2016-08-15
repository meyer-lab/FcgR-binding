function next = PROPRND(current,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
    stdR,stdKx,stdc,stdsigma)
    % Preset next below all minimum thresholds
    next = [lbR*ones(1,6) lbKx lbc*ones(1,2) 1 1 lbsigma] - ones(1,12);
    
    % Generate new logR values
    for j = 1:6
        NEXT = next(j);
        CURRENT = current(j);
        while (NEXT < lbR) || (ubR < NEXT)
            NEXT = CURRENT + twotailexprnd(stdR);
        end
        next(j) = NEXT;
    end
    
    %Generate new logKx value
    NEXT = next(7);
    CURRENT = current(7);
    while (NEXT < lbKx) || (ubKx < NEXT)
        NEXT = CURRENT + twotailexprnd(stdKx);
    end
    next(7) = NEXT;
    
    %Generate new common logs of conversion coefficients
    for j = 8:9
        NEXT = next(j);
        CURRENT = current(j);
        while (NEXT < lbc) || (ubc < NEXT)
            NEXT = CURRENT + twotailexprnd(stdc);
        end
        next(j) = NEXT;
    end
    
    %Generate new avidities    
    v4 = current(10);
    v26 = current(11);
    NEXT10 = next(10);
    NEXT11 = next(11);
    while (NEXT10 < lbv) || (ubv < NEXT10) 
        NEXT10 = v4+randi(3)-2;
    end
    next(10) = NEXT10;
    while (NEXT11 < lbv) || (ubv < NEXT11)
        NEXT11 = v26+randi(3)-2;
    end
    next(11) = NEXT11;
    
    % Generate next standard deviation coefficient
    NEXT = next(12);
    CURRENT = current(12);
    while (NEXT < lbsigma) || (ubsigma < NEXT)
        NEXT = CURRENT + twotailexprnd(stdsigma);
    end
    next(12) = NEXT;
end
%--------------------------------------------------------------------------
function val = twotailexprnd(inversestd)
    % inversestd represents the reciprocal of the standard deviation of the
    % corresponding exponential distribution, which happens to be equal to
    % the mean of the corresponding exponential distribution
    val = exprnd(inversestd);
    temp = randi(2);
    if temp == 1
        val = -val;
    end
end