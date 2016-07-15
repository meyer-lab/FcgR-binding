function tails = DerpyAnalysis(alpha)
    %Load MCMC data
    load('mhsampleResults2.mat')
    
    tails = zeros(2,size(sample,2));
    
    for j = 1:13
        sampleColumn = sample(:,j);
        if j <= 9
            minimum = -20;
            maximum = 5;
        elseif j <= 11
            minimum = 1;
            if j == 10
                maximum = 30;
            else
                maximum = 30;
            end
        else
            minimum = -20;
            maximum = 2;
        end
        for k = 1:2
            %1 for minimum; 2 for maximum
            if j <= 9 || j >= 12
                tails(k,j) = bisection1(sampleColumn,minimum,maximum,alpha,nsamples,k);
            else
%                 tails(k,j) = bisection2(sampleColumn,minimum,maximum,alpha,nsamples,k);
                tails(k,j) = nan;
            end
        end
    end
end
%--------------------------------------------------------------------------
function c = bisection1(sampleColumn,a,b,alpha,nsamples,minormax)
    %%%This function returns the point at which function fun equals zero
    %%%using the bisection algorithm. The closest a and b will converge to
    %%%in the algorithm is a distance 1e-12 apart.
    
    bVal = fun(sampleColumn,b,alpha,nsamples,minormax);
    cVal = fun(sampleColumn,a,alpha,nsamples,minormax);
    
    % Is there no root within the interval?
    if bVal*cVal > 0
        c = nan;
        return;
    end
    
    %In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin
    %with; only implemented for MATLAB Coder
    c = nan;
    %Commence algorithm
    while b - a > 1e-4 || abs(cVal) > 1e-4
        c = (a+b)/2;
        cVal = fun(sampleColumn,c,alpha,nsamples,minormax);
        
        if cVal*bVal >= 0
            b = c;
            bVal = cVal;
        else
            a = c;
        end
    end
end
%--------------------------------------------------------------------------
% function c = bisection2(sampleColumn,a,b,alpha,nsamples,minormax)
    
%--------------------------------------------------------------------------
function diff = fun(sampleColumn,c,alpha,nsamples,minormax)
    if minormax == 1
        test = sampleColumn >= c;
    else
        test = sampleColumn <= c;
    end
    diff = 1-alpha-sum(test)/nsamples;
end