function next = MehRND(current)
    next = zeros(1,11);
    next(1:9) = current(1:9) + normrnd(0,0.1,[1,9]);
    if sum(next(1:9) <= -20) || sum((next(1:9) >= 5))
        next = [25*rand(1,9)-20,randi(4,1,1),randi(26,1,1)];
        return
    end
    
    v4 = current(10);
    v26 = current(11);
    
    while (next(10) < 1) || (4 < next(10)) 
        next(10) = v4+randi(3)-2;
    end
    while next(11) < 1 || 26 < next(11)
        next(11) = v26+randi(3)-2;
    end
end