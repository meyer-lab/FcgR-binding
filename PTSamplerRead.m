pmat = csvread('p.csv');
lnprobmat = csvread('lnprob.csv');
lnlikemat = csvread('lnlike.csv');
pmat = pmat(:,2:length(pmat(1,:)));
lnprobmat = lnprobmat(:,2:length(lnprobmat(1,:)));
lnlikemat = lnlikemat(:,2:length(lnlikemat(1,:)));

ntemps = 10;
nwalkers = 26;
nvars = 12;

nsamples = size(pmat,1);

ptens = zeros(ntemps,nwalkers,nvars,nsamples);
lnprobtens = zeros(ntemps,nwalkers,nsamples);
lnliketens = lnprobtens;

for j = 1:nsamples
    ptens(:,:,:,j) = reshape(pmat(j,:),ntemps,nwalkers,nvars);
    lnprobtens(:,:,j) = reshape(lnprobmat(j,:),ntemps,nwalkers);
    lnliketens(:,:,j) = reshape(lnlikemat(j,:),ntemps,nwalkers);
end

save('PTSamplerData.mat','ptens','lnprobtens','lnliketens','nwalkers',...
    'ntemps','nvars','nsamples')