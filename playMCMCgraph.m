function z = playMCMCgraph(sample,arg)
    z = 5;
    if arg == 0
        for j = 1:11
            for k = 1:11
                plot(sample(:,j),sample(:,k),'.');
                title([num2str(j) ' -- ' num2str(k)]);
                pause
            end
        end
    elseif arg == 1
        for j = 1:11
            hist(sample(:,j),100);
            title(num2str(j));
            pause
        end
    elseif arg == 2
        covariance = cov(sample);
        for j = 1:11
            covariance(j,j) = nan;
        end
%         covariance(7,:) = nan*ones(1,7);
%         covariance(:,7) = nan*ones(7,1);
        bar3(covariance)
        title('Covariance')
    end
end