function diff = playSimAnneal(threeVar, kdBruhns, mfiAdjMean, biCoefMat, ...
    tnpbsa, FcgR1, FcgR2, funcInd, rArg)
    %The threeVar input is a vector. The first element of this vector is an
    %index corresponding to a particular IgG (1 for IgG1, ad nauseam). The
    %second element of the vector corresponds to the valence of the ligand,
    %and the third element corrsponds to the common log of a value of Kx;
    %this third element is NOT an integer.
    %
    %The inputs FcgR1 and FcgR2 are meant to be integers from 1 to 6, each
    %integer from 1 to 6 representing a different FcgR.
    
%     [~,~,comp] = ErrorAvidityChange([3*ones(6,1);threeVar(3);[1;1;1];...
%         threeVar(2)],kdBruhns,mfiAdjMean,biCoefMat,tnpbsa);
    if nargin < 9
        logR = log10(2e4);
    else
        logR = rArg;
    end
    
    if funcInd == 1
        comp = LigandFinder([logR*ones(6,1);threeVar(3);[1;1;1];(threeVar(2))],...
            kdBruhns,mfiAdjMean,biCoefMat,tnpbsa);
    elseif funcInd == 2
        comp = RmultiFinder([logR*ones(6,1);threeVar(3);[1;1;1];(threeVar(2))],...
            kdBruhns,mfiAdjMean,biCoefMat,tnpbsa);
    elseif funcInd == 3
        comp = ClusterFinder([logR*ones(6,1);threeVar(3);[1;1;1];(threeVar(2))],...
            kdBruhns,mfiAdjMean,biCoefMat,tnpbsa);
    else
        error('Input an index "funcInd" from 1 to 3.');
    end

    diff = log10(comp(FcgR1,(threeVar(1))+4)/comp(FcgR2,...
        (threeVar(1))+4));
end