function diff = fun(x, R, vi, kx, viLikdi)
    x = 10.^x;
    diff = R - x*(1+viLikdi*(1+kx*x)^(vi-1));
end