function [ J ] = Errrr2( R )
%Errrr2 An error function meant to be used to help estimate the number of
%receptors on each of our CHO lines.
%   To properly utilize, in the commmand window, type:
%   fmincon(@(x) Errrr2(x),ones(6,1),[],[],[],[],zeros(6,1),1e6*ones(6,1))
%   
%   The result should be approximately equal to:
%   [ 1.5278 ;  2.9234 ; 15.9374 ; 35.4406 ; 9.6195 ; 1.7717]
    

%boundExp contains the expected number of bound immune complexes calculated
%using the simplified equation we have been dealing with. The first four 
%entries are the expected number of IgG1, 2, 3, and 4 immune complexes
%bound to FcgRI, the second four the expected number of IgG1, 2, 3, and 4
%complexes bound with FcgRIIA-Arg, etc.

load 'boundExp2.mat'

%mifAdjMean was calculated by subtracting the background mfi from the mfis
%in each column per each flavor of receptor, taking the nanmean of the
%modified mfis across each row, and multiplying the second to last row by 
%8/7 to account for the missing mfi in Lux's data.

load 'mfiAdjMean2.mat'

a = zeros(192,1);

for j = 1:6
    for k = 1:4
        for l = 1:8
            a(32*(j-1) + 8*(k-1) + l) = (R(j)*boundExp2(j,k) - mfiAdjMean2((4*(j-1)+k),l))^2;
        end
    end
end

J = nansum(a);
end