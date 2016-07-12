%Close all plots
close all

%Load data
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Setting a Kx value shown in Stone to show significant numbers of immne
%complex bound for all avidities 
Kx = 2e-4;
logKx = log10(Kx);

%Assume that the number of FcgRs on each cell is 1000.
R = 1e3;

%Look at number of receptors bound and the number of complexes formed for
%only IgG1
IgG = 1;

%This script assumes that the molar concentration of immune comlplex is the
%same as for TNP-4-BSA from Lux.
L0 = tnpbsa(1);

figure('units','normalized','position',[0.1 0.1 0.8 0.8])
for j = 1:6
    L = zeros(1,26);
    Rmulti = zeros(1,26);
    if j == 1
        color = 'b';
    elseif j == 2
        color = 'g';
    elseif j == 3
        color = 'r';
    elseif j == 4
        color = 'c';
    elseif j == 5
        color = 'y';
    else
        color = 'k';
    end
    for k = 1:26
        L(k) = StoneSolver(R,Kx,k,kdBruhns(j,IgG),L0,biCoefMat);
        Rmulti(k) = RmultiSolver(R,Kx,k,kdBruhns(j,IgG),L0,biCoefMat);
    end
    %Add jitter
%     noiseA = 0.1*(rand(1,26)-0.5);
%     noiseB = 0.01*(rand(1,26)-0.5);
    if j ~=2 && j ~= 5
        subplot(1,2,1)
        plot([1:26],L,[color 'o'])
        hold on
        subplot(1,2,2)
        plot([1:26],Rmulti,[color 'o'])
        hold on
    end
end
subplot(1,2,1)
% title('ICs Bound v. Avidity')
xlabel('Avidity')
ylabel('ICs bound')
subplot(1,2,2)
% title(['Receptor Clusters Formed' char(10) 'v. Avidity'])
xlabel('Avidity')
ylabel('Clusters formed')
subplot(1,2,2)
legend('Fc\gammaRIA','Fc\gammaRIIA','Fc\gammaRIIB','Fc\gammaRIIIA',...
    'Location','NorthWest')
hold off