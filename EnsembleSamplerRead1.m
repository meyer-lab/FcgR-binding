clear;clc;

% Load points from recepnum1Connector1-2.py. In the script, the number of
% walkers is 100, and the number of dimensions is 12.
temp = csvread('pos.csv');
nsamples = size(temp,1);
nwalkers = 100;
ndims = 12;

% Create an array of points output from the sampler
sample = zeros(nwalkers,ndims,nsamples);
for j = 1:nsamples
    sample(:,:,j) = reshape(temp(j,:),nwalkers,ndims);
end

for 