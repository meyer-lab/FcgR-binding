clear;clc;

csvname = input(['Please input the name of the csv whose contents you' char(10)...
    'intend to analyze.' char(10) char(10)]);clc;

disp('Gathering data...')
% Load points from the script. In each script, the number of
% walkers is 100
temp = csvread(csvname);
temp = temp(:,2:size(temp,2));
nsamples = size(temp,1);
nwalkers = 100;
if csvname ~= 'pos1.csv'
    ndims = 12;
else
    ndims = 7;
end

% checkauto = input(['Check autocorrelation for ergodicity test? If so,' char(10)...
%     'please input "pls" in single quotes.' char(10) char(10)]);clc
if 0
    clc
    disp('Plotting...')
    for j = 1:nwalkers
        figure('Units','normalized','Position',[0 0 1 1])
        for k = 1:ndims
            subplot(3,4,k)
            autocorr(temp(:,ndims*(j-1)+k),1000)
            title(num2str(j))
        end
        pause(2)
        close
    end
end

% Plot data
sample = reshape(temp,ndims,nwalkers*nsamples);
sample = sample';

if csvname ~= 'pos1.csv'
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
else
    for j = 1:7
        if j < 2
            name = 'log Fc\gammaR';
        elseif j == 2
            name = 'log Kx Coefficient';
        elseif j < 5
            if j == 3
                tnpbsa = 'TNP-4-BSA';
            else
                tnpbsa = 'TNP-26-BSA';
            end
            name = ['log Conversion Coefficient ' tnpbsa];
        elseif j < 7
            if j == 5
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
end
    