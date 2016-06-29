function [good, goodfit, meh] = pseudoAlgorithm(nsamples,goodsize,mehsize,...
    kdBruhns,tnpbsa,mfiAdjMean,best,meanPerCond,stdPerCond,biCoefMat)

good = zeros(goodsize,11,nsamples*(goodsize+mehsize)+1);
meh = zeros(mehsize,11,nsamples+1);
good(:,:,1) = [25*rand(goodsize,9)-20,randi(4,goodsize,1),randi(26,goodsize,1)];
meh(:,:,1) = [25*rand(mehsize,9)-20,randi(4,mehsize,1),randi(26,mehsize,1)];

goodfit = zeros(goodsize,nsamples*(goodsize+mehsize)+1);
for j = 1:goodsize
    goodfit(j,1) = PDF(good(j,:,1),kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,...
        meanPerCond,stdPerCond);
end

for j = 1:nsamples
    for k = 1:mehsize
        meh(k,:,j+1) = MEHRND(meh(k,:,j));
    end

    for k = 1:goodsize
        for l = 1:mehsize
            temp = PROPRND(meh(l,:,j));
            tempfit = PDF(temp,kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,...
                meanPerCond,stdPerCond);
            goodtemp = good(k,:,(j-1)*(goodsize+mehsize)+l);
            goodtempfit = goodfit(k,(j-1)*(goodsize+mehsize)+l);
            if tempfit - goodtempfit < 0
                if rand < exp(tempfit-goodtempfit)
                    good(k,:,1+(j-1)*(goodsize+mehsize)+l) = temp;
                    goodfit(k,1+(j-1)*(goodsize+mehsize)+l) = tempfit;
                else
                    good(k,:,1+(j-1)*(goodsize+mehsize)+l) = goodtemp;
                    goodfit(k,1+(j-1)*(goodsize+mehsize)+l) = goodtempfit;
                end
            else
                good(k,:,1+(j-1)*(goodsize+mehsize)+l) = temp;
                goodfit(k,1+(j-1)*(goodsize+mehsize)+l) = tempfit;
            end
        end
        for l = 1:goodsize
            temp = PROPRND(good(l,:,(j-1)*(goodsize+mehsize)+mehsize+l));
            tempfit = PDF(temp,kdBruhns,mfiAdjMean,biCoefMat,tnpbsa,...
                meanPerCond,stdPerCond);
            goodtemp = good(k,:,(j-1)*(goodsize+mehsize)+mehsize+l);
            goodtempfit = goodfit(k,(j-1)*(goodsize+mehsize)+mehsize+l);
            if tempfit - goodtempfit < 0
                if rand < exp(tempfit-goodtempfit)
                    good(k,:,1+(j-1)*(goodsize+mehsize)+mehsize+l) = temp;
                    goodfit(k,1+(j-1)*(goodsize+mehsize)+mehsize+l) = tempfit;
                else
                    good(k,:,1+(j-1)*(goodsize+mehsize)+mehsize+l) = goodtemp;
                    goodfit(k,1+(j-1)*(goodsize+mehsize)+mehsize+l) = goodtempfit;
                end
            else
                good(k,:,1+(j-1)*(goodsize+mehsize)+mehsize+l) = temp;
                goodfit(k,1+(j-1)*(goodsize+mehsize)+mehsize+l) = tempfit;
            end
        end
    end
end
end