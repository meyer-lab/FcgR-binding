function [ J ] = Errrr( R )
%Errrr An error function meant to be used to help estimate the number of
%receptors on each of our CHO lines.
%   To properly utilize, in the commmand window, type:
%   fmincon(@(x) Errrr(x),5*ones(6,1),[],[],[],[],zeros(6,1),1e6*ones(6,1))
%   
%   The result should be approximately equal to:
%   [0.0007;0.0013;0.0008;0.013;0.0007;0.0006]
    

%boundExp contains the expected number of bound immune complexes calculated
%using the simplified equation we have been dealing with. The first four 
%entries are the expected number of IgG1, 2, 3, and 4 immune complexes
%bound to FcgRI, the second four the expected number of IgG1, 2, 3, and 4
%complexes bound with FcgRIIA-Arg, etc.

load 'boundExp.mat'

%mifAdjMean was calculated by subtracting the background mfi from the mfis
%in each column per each flavor of receptor, taking the nanmean of the
%modified mfis across each row, ans multiplying the second to last row by 
%8/7 to account for the missing mfi in Lux's data.

load 'mfiAdjMean.mat'

a = zeros(6,1);

for j = 1:6
    a(j) = sum(mfiAdjMean(((j-1)*4+1):((j-1)*4+4)));
end

b = sum(boundExp(((j-1)*4+1):((j-1)*4+4)));
J = 0.5*sum((b - R .* a) .^ 2);
end