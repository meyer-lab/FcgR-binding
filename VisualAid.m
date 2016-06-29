clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Load aicbest; this is the point which yields the lowest AIC with both
%simulated annealing and MATLAB's genetic algorithm. This is to get the
%best fits for the TNP-BSA-to-MFI conversion factors
load('aicbest.mat')
%Common logs of TNP-BSA-to-MFI conversion factors
convfac = aicbest(8:9)';

%Dimensions correspond to IgG, IgG (the repeat is intentional; see below),
%FcgR, TNP-BSA avidity, and Kx, respectively. The script will pore through 
%Kx values by integer order of magnitude ranging from -10 to -3.
utilTens = zeros(4,4,6,26,8);

%Vector representing Kx orders of magnitude
ordmagKx = [-10:-3];

%Iterate through TNP-4-BSA avidities, TNP-26-BSA avidities, and Kx orders
%of magnitude
for j = 1:26
    for k = 1:8
        x = [3*ones(6,1);ordmagKx(k);convfac;1;j];
        [~,~,mfiExpPre] = ErrorAvidityChange(x,kdBruhns,...
            mfiAdjMean,biCoefMat,tnpbsa);
        for l = 1:6
            tempMat = zeros(4);
            for m = 1:4
                for n = 1:4
                    tempMat(m,n) = mfiExpPre(l,m+4) - mfiExpPre(l,n+4);
                end
            end
            utilTens(:,:,l,j,k) = tempMat;
        end
    end
end