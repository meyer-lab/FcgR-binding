%load binding affinities and molarities of TNP-X-BSA
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, TempKx] = loadData();

%Arbitrarily-chosen number of receptors expressed
R = 1000;

%Molarity of TNP-4-BSA from Nimmerjahn lab's paper arbitrarily chosen
L = tnpbsa4;

Kd = kdBruhns;

%Kx arbitrarily set as the value of Kx which led to the best fit in
%RegressionAndResiduals
Kx = TempKx;

%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%Function which will be used with fzero to find the Req for each
%combination of IgG and FcR per valency.
ReqFunc = @(Reqi, Ri, Kdi, Li, vi) Ri - Reqi*(1+vi*Li/Kdi*(1+Kx*Reqi)^(vi-1));
fzeroOpt = optimset('Display','off');

%Iterate over IgGs
for j = 1:4
    %Name of IgG
    if j == 1
        name = 'IgG1';
    elseif j == 2
        name = 'IgG2';
    elseif j == 3
        name = 'IgG3';
    else
        name = 'IgG4';
    end
    figure
    %Iterate over FcgRs
    for k = 1:6
        %Set Kd value
        KdSpec = Kd(k,j);
        %Set curve colors
        if k == 1
            color = 'k';
        elseif k == 2
            color = 'b';
        elseif k == 3
            color = 'g';
        elseif k == 4
            color = 'r';
        elseif k == 5
            color = 'c';
        else
            color = 'm';
        end
        
        %Pre-allocate data for vector of predicted expression values
        yVec = zeros(1,26);
        %Create vector of valency values
        xVec = [1:26];
        
        for l = 1:26
            %Calculate Req per valency
            Req = fzero(@(x) ReqFunc(x,R,KdSpec,L,l),-1,fzeroOpt);
            
            %Calculating expression per valency
            temp = zeros(1,l);
            for m = 1:l
                temp(m) = biCoefMat(m,l)*Kx^(m-1)*L/KdSpec*Req^m;
            end
            yVec(l) = nansum(temp);
        end
        
        %Plot curves per IgG
        plot(xVec,yVec,[color 'x-']);
        hold on
    end
    %Label axes and title graph
    xlabel('Valency');
    ylabel('Number of Ligand Bound');
    title(name);
    %New graph
    hold off
    savefig(name);
end