[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, TempKx, bestHomogeneicFit, bestHomogeneicKx] = loadData();

R = bestHomogeneicFit;
v = [4;26];
L4 = tnpbsa4;
L26 = tnpbsa26;
Kx = bestHomogeneicKx;

mfiAdjMean = [mfiAdjMean4 mfiAdjMean26];
for j = 1:24
    for k = 1:8
        if mfiAdjMean(j,k) < 0
            mfiAdjMean(j,k) = 0;
        end
    end
end

factor = 3/100*log(10);

temp1 = [0:1000];
Kd = 1e-8 * factor .^ temp1;
expr = zeros(size(Kd));

ReqFunc = @(Reqi, Li, kdi, vi) R - Reqi*(1+vi*Li/kdi*(1+Kx*Reqi)^(vi-1));
fzeroOpt = optimset('Display','off');

for j = 1:length(temp1)
    Req4(j,k) = fzero(@(x) ReqFunc(x,L4,Kd(j),4), -1, fzeroOpt);
    Req26(j,k) = fzero(@(x) ReqFunc(x,L26,Kd(j),26), -1, fzeroOpt);
end