clear;clc;

disp('Gathering data...')
% Load points from recepnum1Connector1-2.py. In the script, the number of
% walkers is 100, and the number of dimensions is 12.
temp = csvread('pos.csv');
temp = temp(:,2:size(temp,2));
nsamples = size(temp,1);
nwalkers = 100;
ndims = 12;

% clc
% disp('Plotting...')
% for j = 1:nwalkers
%     figure('Units','normalized','Position',[0 0 1 1])
%     for k = 1:ndims
%         subplot(3,4,k)
%         autocorr(temp(:,ndims*(j-1)+k),20)
%         title(num2str(j))
%     end
%     pause(2)
%     close
% end

% Plot data
sample = reshape(temp,ndims,nwalkers*nsamples);
sample = sample';

for j = 1:12
    if j < 7
        name = ['log Fc\gammaR No. ' num2str(j)];
    elseif j == 7
        name = 'log Kx Coefficient';
    elseif j < 10
        if j == 8
            tnpbsa = 'TNP-4-BSA';
        else
            tnpbsa = 'TNP-26-BSA';
        end
        name = ['log Conversion Coefficient ' tnpbsa];
    elseif j < 12
        if j == 10
            tnpbsa = 'TNP-4-BSA';
        else
            tnpbsa = 'TNP-26-BSA';
        end
        name = ['Avidity' tnpbsa];
    else
        name = 'log std Coefficient';
    end
    figure('units','normalized','position',[0 0 1 1])
    plot(sample(:,j))
    title(name)
end
    