% x = [0:0.1:1000];
% y = zeros(size(x));
% for j = 2:length(x)
%     y(j-1) = log10(x(j));
% end
% 
% hist(y,100)
% hold on
% w = [0:0.01:3];
% z = 10.^w;
% 
% plot(w,z)

%Loading basic parameters
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, bestHomogeneicFit, bestHomogeneicKx] = loadData;

%Set valencies
v = [4;26];
%Create vector of TNP-BSA molarities
tnpbsa = [tnpbsa4;tnpbsa26];
%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

thing1 = rand(7,10000);
thing2 = zeros(size(thing1));
thing3 = zeros(1,length(thing1));
for j = 1:length(thing1)
    for k = 1:7
        thing2(k,j) = log10(thing1(k,j))+1;
    end
    thing3(j) = Error(thing2(:,j),kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa);
end

mcmcAdj = nanmean(thing3);
save('mcmcAdj.mat','mcmcAdj')