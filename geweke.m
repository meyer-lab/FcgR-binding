function [result, scores] = geweke(sample, stringency)
    %%% Performs the Geweke diagnostic on the sample resulting from a
    %%% Metropolis-Hastings MCMC to measure whether the sample has reached
    %%% ergodicity. This function will only accept samples of size 100 or
    %%% greater and will otherwise throw an error. a matrix of Student's t-
    %%% test statistics is the output of this function. They must all be 
    %%% within the desired range according to typical t-test interpretation
    %%% in order for the diagnostic to be interpreted as positive.
    
    sz = size(sample,1);
    if sz < 300
        error(['The function geweke can only handle samples of at least' ...
            '300 in size.'])
    end
    dim = size(sample,2);
    
    lowersize = ceil(sz/10);
    upperfloor = floor(sz/2);
    uppersize = sz-upperfloor+1;
    lower = sample(1:lowersize,:);
    upper = sample(uppersize:sz,:);
    
    meansl = mean(lower);
    meansu = mean(upper);
    covl = cov(lower);
    covu = cov(upper);
    
    scores = zeros(dim);
    for j = 1:dim
        for k = 1:j
            if j ~= k
                gammal = (lower(:,j)-meansl(j)).*(lower(:,k)-meansl(k));
                gammau = (upper(:,j)-meansu(j)).*(upper(:,k)-meansu(k));
                gammeanl = mean(gammal);
                gammeanu = mean(gammau);
                varl = var(gammal);
                varu = var(gammau);
                scores(j,k) = (gammeanl-gammeanu)/sqrt(varl/lowersize+...
                    varu/uppersize);
            else
                scores(j,j) = (meansl(j)-meansu(j))/sqrt(covl(j,j)/lowersize+...
                    covu(j,j)/uppersize);
            end
        end
    end
    tests = normpdf(scores);
    for j = 1:dim^2
        if tests(j) > 0.5
            tests(j) = 1-tests(j);
        end
    end
    fail = (tests < stringency);
    if sum(sum(fail)) > 0
        result = 'Fail';
    else
        result = 'Pass';
    end
end