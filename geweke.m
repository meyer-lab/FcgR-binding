function scores = geweke(sample)

    sz = size(sample,1);
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
    
    scores = nan*ones(dim);
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
end