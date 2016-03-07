load 'mfiAdjMean.mat'
load 'mfiDiff.mat'

%A graphic representation of the data from Lux's lab
bar3(mfiAdjMean);
title('Normalized MFIs from Anja Lux')
hold on

%A graphic representation of the residuals of Lux's data against our model
figure
bar3(mfiDiff);
title('Calculated Errors in Normalized MFI (Expected minus Actual)')