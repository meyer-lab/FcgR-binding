clc;clear;

%%%Establish constants
%Load data
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, ~, ~, best] = loadData;
%Valencies and TNP-X-BSA molarities
v = [4;26];
tnpbsa = [tnpbsa4;tnpbsa26];
%Create matrix of binomial coefficients
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%%%Set up for HMC
nsamples = 100;
stepsize = 0.3;
leap = stepsize/2;  %Reference to leapfrog method
%%CHANGE startPos TO SUIT NEEDS
startPos = 10*rand(7,1);
startMom = 1*rand(7,1);
pos = startPos;
mom = startMom;
mom = mom-leap*(jacobianest(@(pos) Error(pos+leap,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa,pos)))*pos;
for j = 1:nsamples-1
    pos = pos+stepsize*mom;
    

