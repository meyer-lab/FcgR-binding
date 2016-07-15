function next = PROPRND(current)
    next = -ones(1,13);
    while max(next(1:6) < 0)
        next(1:9) = current(1:9) + normrnd(0,0.039,[1,9]);
    end
    next(12:13) = current(12) + normrnd(0,0.01,[1,1]);
    
    v4 = current(10);
    v26 = current(11);
    
    while next(10) < 1 || 30 < next(10) 
        next(10) = v4+randi(3)-2;
%         next(10) = v4+(2*(randi(2)-1)-1)*exprnd(1);
    end
    while next(11) < 1 || 30 < next(11)
        next(11) = v26+randi(3)-2;
%         next(11) = v26+(2*(randi(2)-1)-1)*exprnd(1);
    end
end