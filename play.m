mfi = csvread('Luxetal2013-Fig2B.csv',2,2);
mfi(29,1) = nan;

mfiAdj = zeros(size(mfi));
for j = 1:6
    for k = 1:8
        mfiAdj(5*(j-1)+2:5*j,k) = mfi(5*(j-1)+2:5*j,k) - mfi(5*(j-1)+1,k);
    end
end
mfiAdj(1:5:end,:) = [];

% bar3(mfiAdj)
% 
% mfiAdjTrue = zeros(size(mfiAdj));
% % for j = 1:6
% %     for k = 1:8
% %         mfiAdjTrue(4*(j-1)+1:4*(j-1)+4,k) = nanmean(mfiAdj(4*(j-1)+1:4*(j-1)+4,k)) * ones(4,1);
% %     end
% % end
% for j = 1:4
%     mfiAdjTrue(:,j) = mfiAdj(:,j) / nanmean([mfiAdj(:,j); mfiAdj(:,j+4)]);
%     mfiAdjTrue(:,j+4) = mfiAdj(:,j+4) / nanmean([mfiAdj(:,j); mfiAdj(:,j+4)]);
% end
% 
% mfiAdjTrue2 = zeros(size(mfiAdj));
% for j = 1:8
%     mfiAdjTrue2(:,j) = mfiAdj(:,j) / nansum(mfiAdj(:,j));
% end
% bar3(mfiAdjTrue2)

mfiAdjShow = zeros(size(mfiAdj));
for j = 1:8
    mfiAdjShow(:,j) = nanmean(mfiAdj(:,j)) * ones(24,1);
end

bar3(mfiAdjShow)
xlabel('Column #')
ylabel('Row #')

show = zeros(1,4);
for j = 1:4
    show(j) = mfiAdjShow(1,j+4) / mfiAdjShow(1,j);
end