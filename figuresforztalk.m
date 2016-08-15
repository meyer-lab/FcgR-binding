clear;clc;close all

%% Normalized MFIs
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData();
mfiAdjMean2 = [];
for j = 1:2
    mfiAdjMean2 = [mfiAdjMean2 nanmean(mfiAdjMean(:,(4*(j-1)+1):(4*j)),2)];
end

mfiAdjMeanL = [nanmin(mfiAdjMean(:,1:4),[],2) nanmin(mfiAdjMean(:,5:8),[],2)];
mfiAdjMeanU = [nanmax(mfiAdjMean(:,1:4),[],2) nanmax(mfiAdjMean(:,5:8),[],2)];

a = figure('color',[1 1 1]);
set(a,'Units','normalized','Position',[0 0 1 1]);
for j = 1:6
    subplot(3,2,j)
    hold on
    for k = 1:4
        if k == 1
            col = 'b';
        elseif k == 2
            col = 'r';
        elseif k == 3
            col = 'k';
        else
            col = 'g';
        end
        for l = 1:2
            if l == 1
                shp = 'x';
            else
                shp = 'o';
            end
            errorbar(20+2*(k-1)+l,mfiAdjMean2(4*(j-1)+k,l),...
                mfiAdjMeanL(4*(j-1)+k,l),mfiAdjMeanU(4*(j-1)+k,l),...
                [col shp],'LineWidth',1.5,'MarkerSize',8)
            set(gca,'xtick',[])
        end
        if j == 1
            str = 'IA';
        elseif j == 2
            str = 'IIA-131R';
        elseif j == 3
            str = 'IIA-131H';
        elseif j == 4
            str = 'IIB';
        elseif j == 5
            str = 'IIIA-158F';
        else
            str = 'IIIA-158V';
        end
        xlabel(['Fc\gammaR' str])
        ylabel('Normalized MFI')
    end
end
frame = getframe(a);
image = frame2im(frame);
[imind, cm] = rgb2ind(image,256);
imwrite(imind,cm,'mfiAdjMeanTable.jpg','JPEG')

figure('color',[1 1 1])
text(0.1,0.5,['\color{blue} IgG1' char(10)...
    '\color{red} IgG2' char(10)...
    '\color{black} IgG3' char(10)...
    '\color{green} IgG4'],'FontWeight','bold','FontSize',16)

%% Maximum difference in order of magnitude of ligand bound/receptors
%% clustered/clusters formed

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

a = figure('units','normalized','position',[0.1 0.1 0.8 0.8],'color',[1 1 1]);
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
xlabel('Effective avidity')
ylabel('ICs bound')
title('Number of ICs bound as a function of avidity')
subplot(1,2,2)
xlabel('Avidity')
ylabel('Clusters formed')
title('Number of receptors clustered as a function of avidity')
subplot(1,2,2)
legend('Fc\gammaRIA','Fc\gammaRIIA','Fc\gammaRIIB','Fc\gammaRIIIA',...
    'Location','NorthWest')
frame = getframe(a);
image = frame2im(frame);
[imind,cm] = rgb2ind(image,256);
imwrite(imind,cm,'ligandvsclustered.jpg','JPEG')
hold off

load('DiffCompare.mat')

for j = 1:2
    if j == 1
        bigDiff = bigDiffLigand;
    else
        bigDiff = bigDiffRmulti;
    end
    for k = 1:6
        for l = 1:6
            if k ~= l
                bigDiff(1,k,l) = log10(kdBruhns(k,bigDiff(1,k,l))/...
                    kdBruhns(l,bigDiff(1,k,l)));
            end
        end
    end
    if j == 1
        XbigDiffLigand = bigDiff;
    else
        XbigDiffRmulti = bigDiff;
    end
end

style = 'k.';
figure('color',[1 1 1])

for j = 1:6
    for k = 1:6
        if j ~= k
            plot3(XbigDiffLigand(1,j,k),XbigDiffLigand(2,j,k),XbigDiffLigand(3,j,k),style)
        end
    end
end

% figure(4);
% hold on
% for j = 1:6
%     for k = 1:6
%         if j ~= k
%             if 
%             plot3(XbigDiffLigand(1,j,k),XbigDiffLigand(2,j,k),XbigDiffLigand(3,j,k))
%         end
%     end
% end
% xlabel('Common log of K_D ratio')
% ylabel('Avidity')
% title('Two modes of IC Design')
% 
% view([0 0 -1])

b = figure('color',[1 1 1]);
hold on
color = 'brkg';
for j = 1:6
    for k = 1:4
        whattoplot = zeros(1,39);
        whattoplot(7*(j-1)+k) = kdBruhns(j,k+6);
        bar(whattoplot,color(k))
    end
end
legend('IgG1','IgG2','IgG3','IgG4','Location','EastOutside')
set(gca,'xtick',[],'YScale','log')
ylabel('Affinity')
set(b,'Units','normalized','Position',[0 0 0.5 1]);
frame = getframe(b);
image = frame2im(frame);
[imind,cm] = rgb2ind(image,256);
imwrite(imind,cm,'KdsforFcgRsIgGs.jpg','JPEG')

new = figure;
text(0.1,0.5,['X -> TNP-4-BSA' char(10) 'O -> TNP-26-BSA'])
frame = getframe(new);
image = frame2im(frame);
[imind,cm] = rgb2ind(image,256);
imwrite(imind,cm,'lastminute.jpg','JPEG')