function next = PROPRND2(current)
    next = zeros(1,6);
    next(1:4) = current(1:4) + normrnd(0,0.039,[1,4]);
    
    v4 = current(5);
    v26 = current(6);
    
    while next(5) < 1 || 4 < next(5) 
        next(5) = v4+randi(3)-2;
    end
    while next(6) < 1 || 26 < next(6)
        next(6) = v26+randi(3)-2;
    end
end