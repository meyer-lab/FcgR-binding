function next = PROPRND(current)
    next = -ones(1,7);
    while max(next(1) < 0)
        next(1:4) = current(1:4) + normrnd(0,0.039,[1 4]);
    end
    next(7) = current(7) + normrnd(0,0.01);
    
    v4 = current(5);
    v26 = current(6);
    
    while next(5) < 1 || 30 < next(5) 
        next(5) = v4+randi(3)-2;
%         next(10) = v4+(2*(randi(2)-1)-1)*exprnd(1);
    end
    while next(6) < 1 || 30 < next(6)
        next(6) = v26+randi(3)-2;
%         next(11) = v26+(2*(randi(2)-1)-1)*exprnd(1);
    end
end