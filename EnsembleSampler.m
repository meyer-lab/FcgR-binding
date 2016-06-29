%Load basic parameters
[kd, tnpbsa, mfiAdjMean, kdBruhns, best, meanPerCond, stdPerCond] = loadData;

%Create matrix of binomial coefficients
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

ensSize = 10;
nsamples = 1000;

ensemble = [25*rand(ensSize,1:9)-20,randi(4,ensSize,ensSize,1),randi(26,ensSize,1)];


