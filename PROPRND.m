function next = PROPRND(current)
    next = zeros(1,11);
    next(1:9) = current(1:9) + normrnd(0,0.039,[1,9]);
    
    v4 = current(10);
    v26 = current(11);
    
    while next(10) < 1 || 4 < next(10) 
        next(10) = v4+randi(3)-2;
    end
    while next(11) < 1 || 26 < next(11)
        next(11) = v26+randi(3)-2;
    end
end