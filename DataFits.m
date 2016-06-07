[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, TempKx, bestHomogeneicFit, bestHomogeneicKx] = loadData();

%Establishing key parameters. bestHomogeneicFit and bestHomogeneicKx are,
%respectively, the receptor expression level and Kx value which yield the 
%best fit granted all receptors have equal expression
R = bestHomogeneicFit;
L4 = tnpbsa4;
L26 = tnpbsa26;
Kx = bestHomogeneicKx;

%A matrix of values of several relevant binomial coefficients
biCoefMat = zeros(2,26);
for j = 1:4
    biCoefMat(1,j) = nchoosek(4,j);
end
for j = 1:26
    biCoefMat(2,j) = nchoosek(26,j);
end

%The value by which 10e-8 must be multuplied 1000 times to become 10e-4
factor = 10^(8/1000);

%x-axis range of Kd values
temp1 = [0:1000];
Kd = 1e-8 * factor .^ temp1;

%pre-allocating expression levels for each curve, which will be shown on
%the y-axis
expression4 = zeros(size(Kd));
expression26 = zeros(size(Kd));

%Finding Req per Kd per valency
Req4 = zeros(1,length(temp1));
Req26 = zeros(1,length(temp1));

ReqFunc = @(Reqi, Li, kdi, vi) R - Reqi*(1+vi*Li/kdi*(1+Kx*Reqi)^(vi-1));
fzeroOpt = optimset('Display','off');

for j = 1:length(temp1)
    Req4(j) = fzero(@(x) ReqFunc(x,L4,Kd(j),4), 0, fzeroOpt);
    Req26(j) = fzero(@(x) ReqFunc(x,L26,Kd(j),26), 0, fzeroOpt);
    
    %Finding the expression level per Kd per valency
    expression4(j) = sum(biCoefMat(1,1:4).*Kx.^([0:3]).*(L4/Kd(j)*Req4(j).^[1:4]));
    expression26(j) = sum(biCoefMat(2,1:26).*Kx.^([0:25]).*(L26/Kd(j)*Req26(j).^[1:26]));
end

%Graphing curves
figure

semilogx(Kd,expression4,'b')
hold on
semilogx(Kd,expression26,'r')
hold on

%Turning negative normalized MFIs into zeros
mfiAdjMean = [mfiAdjMean4 mfiAdjMean26];
for j = 1:24
    for k = 1:8
        if mfiAdjMean(j,k) < 0
            mfiAdjMean(j,k) = 0;
        end
    end
end

%Plotting normalized MFIs from Nimmerjahn lab against relevant Kd values
for j = 1:6
    for k =1:4
        semilogx(kdBruhns(j,k)*ones(1,4),mfiAdjMean(4*(j-1)+k,1:4),'xb');
        hold on
        semilogx(kdBruhns(j,k)*ones(1,4),mfiAdjMean(4*(j-1)+k,5:8),'xr');
        hold on
    end
end

%Labelling axes
xlabel('Kd');
ylabel('Expression Level');
title('Recpetor Expression Level v. Kd');

hold off

%Saving figure
savefig('ReceptorExpressionvKd.fig')