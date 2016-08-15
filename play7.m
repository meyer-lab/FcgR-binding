clear;clc;

%Loading basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Load tempbest
load('best.mat')

%Load gong sound
load gong

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 30
biCoefMat = zeros(30,30);
for j = 1:30
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Lower and upper bounds of various parameters
lbR = 0;
ubR = 8;
lbKx = -20;
ubKx = 0;
lbc = -20;
ubc = 5;
lbv = 1;
ubv = 30;
lbsigma = -20;
ubsigma = 2;
%%%Note carefully that start is a row vector that must be transposed to be
%%%put into Error
start = best;
%standard deviation of exponential distribution
stdR = 0.85;
stdKx = 0.85;
stdc = 0.85;
stdsigma = 0.4;
%Number of samples for MCMC
nsamples = input('Number of samples:\n');
clc;
%Log probability proposal distribution
%proppdf = @(x,y) -sum(([x(1:9), x(12:13)]-[y(1:9), y(12:13)]).^2);
% proppdf = @(x,y) 1/(1+max(10.^x1:6))-min(10.^x(1:6)));
proppdf = @(x,y) PROPPDF(x,y,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
    stdR,stdKx,stdc,stdsigma);
%Pseudo-random generator of new points to test; 0.039 gives accept of about
%0.23 for 7 parameters
proprnd = @(x) PROPRND_mex(x,lbR,ubR,lbKx,ubKx,lbc,ubc,lbv,ubv,lbsigma,ubsigma,...
    stdR,stdKx,stdc,stdsigma);
%Probability distribution of interest
pdf = @(x) NormalError_mex(x,kdBruhns,mfiAdjMean,tnpbsa,meanPerCond,...
    biCoefMat);

%Run Metropolis-Hastings algorithm
[sample,accept] = mhsample(start,nsamples,'logpdf',pdf,'logproppdf',proppdf, ...
    'proprnd',proprnd,'symmetric',0,'burnin',1000);

%Collect the errors for each element in the chain. Also, collect the list
%of all displacements in log space and "standard" space from the best fit
%point. From these displacements, find the distances in log space and in
%standard space.
likelihoods = zeros(nsamples,1);
distfrombest = likelihoods;
for j = 1:nsamples
    likelihoods(j) = NormalError_mex(sample(j,:),kdBruhns,mfiAdjMean,tnpbsa,...
        meanPerCond,biCoefMat);
    distfrombest(j) = sum((best-sample(j,:)).^2);
end
testsample = sample;
testsample(:,1:9) = 10.^sample(:,1:9);
testsample(:,12) = 10.^sample(:,12);

fig = figure('color',[1 1 1],'Units','normalized','Position',[0 0 1 1]);
plot(sample);
xlabel('Iteration')
ylabel('Order of magnitude')
legend('Fc\gammaRIA expression','Fc\gammaRIIA-131R expression',...
    'Fc\gammaRIIA-131H expression','Fc\gammaRIIB expression',...
    'Fc\gammaRIIIA-158F expression','Fc\gammaRIIIA-158V expression',...
    'K_X','Conversion factor, TNP-4-BSA','Conversion factor, TNP-26-BSA',...
    'Avidity, TNP-4-BSA','Avidity, TNP-26-BSA','\sigma^*','Location',...
    'EastOutside')
frame = getframe(fig);
image = frame2im(frame);
[im, cm] = rgb2ind(image,256);
imwrite(im,cm,'MCMCTrace.jpg','JPEG')

color = 'color';
Units = 'Units';
normalized = 'normalized';
pos = 'Position';
for j = 1:12
    if (j == 7) || (j == 1)
        figname = ['fig' num2str(j)];
        eval([figname ' = figure(color,[1 1 1],Units,normalized,pos,[0 0 1 1]);'])
    end
    modind = mod(j,6);
    if modind == 0
        modind = 6;
    end
    subplot(2,3,modind)
    hist(sample(:,j),100)
    if (j == 10) || (j == 11)
        string = 'Value';
    else
        string = 'Order of magnitude';
    end
    xlabel(string)
    ylabel('Frequency')
    
    if (j ~= 10) && (j ~= 11)
        a = gca;
        powers = get(a,'XTick');
        tobeset = {};
        for k = 1:length(powers)
            tobeset{k} = ['10^{' num2str(powers(k)) '}'];
        end
        set(a,'XTickLabel',tobeset)
    end
    
    if j < 7
        if j == 1
            name = 'RIA';
        elseif j == 2
            name = 'RIIA-131R';
        elseif j == 3
            name = 'RIIA-131H';
        elseif j == 4
            name = 'RIIB';
        elseif j == 5
            name = 'RIIIA-158F';
        else
            name = 'RIIIA-158V';
        end
        title(['Fc\gamma' name ' expression'])
    elseif j == 7
        title('K_X')
    elseif j < 10
        if j == 8
            num = num2str(4);
        else
            num = num2str(26);
        end
        title(['Ligand-to-MFI conversion factor, TNP-' num '-BSA'])
    elseif j < 12
        if j == 10
            num = num2str(4);
        else
            num = num2str(26);
        end
        title(['Avidity of TNP-' num '-BSA'])
    else
        title('\sigma^*')
    end
    
    if (j == 6) || (j == 12)
        eval(['frame = getframe(fig' num2str(j-5) ');'])
        image = frame2im(frame);
        [im, cm] = rgb2ind(image,256);
        imwrite(im,cm,[figname '.jpg'],'JPEG')
    end
end

sound(y);