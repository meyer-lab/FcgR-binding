load 'mfiAdjMean2.mat'
load 'mfiDiff2.mat'

%A graphic representation of the data from Lux's lab
bar3(mfiAdjMean2);
title('Normalized MFIs from Anja Lux')
hold on

%A graphic representation of the residuals of Lux's data against our model
figure
bar3(mfiDiff2);
title('Calculated Errors in Normalized MFI (Expected minus Actual)')