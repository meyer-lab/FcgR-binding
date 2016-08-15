clear;clc;

load('PTSamplerData.mat')

% ptens is of the dimensions ntemps,nwalkers,nvars,nsamples

for j = 1:ntemps
    str = num2str(j);
    eval(['ptens' str ' = ptens(j,:,:,:);'])
    eval(['ptens' str ' = permute(ptens' str ',[4 3 2 1]);'])
    eval(['pvec' str ' = [];'])
    for k = 1:nwalkers
        eval(['pvec' str ' = [pvec' str '; ptens' str '(:,:,k)];'])
    end
    subplot(2,5,j)
    eval(['plot(pvec' str ')'])
end

