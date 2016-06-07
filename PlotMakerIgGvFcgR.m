%load parameters
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, TempKx, bestHomogeneicFit, bestHomogeneicKx] = loadData();

for j = 1:2
    %1000 is an arbitrarily-chosen number of receptors expressed, which seems
    %reasonable based on what I have found from Google searches.
    %bestHomogeneicFit is the value for receptor expression which yields the
    %best fit assuming all cell lines have equal levels of receptor expression
    if j == 1
        R = 1000;
    else
        R = bestHomogeneicFit;
    end
    
    %Molarity of TNP-4-BSA from Nimmerjahn lab's paper arbitrarily chosen
    L = tnpbsa4;

    Kd = kdBruhns;

    %Kx arbitrarily set as the value of Kx which led to the best fit in
    %RegressionAndResiduals
    Kx = bestHomogeneicKx;

    %Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
    %all i from 1 to v for all v from 1 to 26
    biCoefMat = zeros(26,26);
    for k = 1:26
        for l = 1:k
            biCoefMat(l,k) = nchoosek(k,l);
        end
    end

    %Function which will be used with fzero to find the Req for each
    %combination of IgG and FcR per valency.
    ReqFunc = @(Reqi, Ri, Kdi, Li, vi) Ri - Reqi*(1+vi*Li/Kdi*(1+Kx*Reqi)^(vi-1));
    fzeroOpt = optimset('Display','off');

    %Iterate over IgGs
    for k = 1:4
        %Name of IgG
        if k == 1
            name = 'IgG1';
        elseif k == 2
            name = 'IgG2';
        elseif k == 3
            name = 'IgG3';
        else
            name = 'IgG4';
        end
        figure
        %Iterate over FcgRs
        for l = 1:6
            %Set Kd value
            KdSpec = Kd(l,k);
            %Set curve colors
            if l == 1
                color = 'k';
            elseif l == 2
                color = 'b';
            elseif l == 3
                color = 'g';
            elseif l == 4
                color = 'r';
            elseif l == 5
                color = 'c';
            else
                color = 'm';
            end
        
            %Pre-allocate data for vector of predicted expression values
            yVec = zeros(1,26);
            %Create vector of valency values
            xVec = [1:26];
        
            for m = 1:26
                %Calculate Req per valency
                Req = fzero(@(x) ReqFunc(x,R,KdSpec,L,m),-1,fzeroOpt);
            
                %Calculating expression per valency
                temp = zeros(1,m);
                for n = 1:m
                    temp(n) = biCoefMat(n,m)*Kx^(n-1)*L/KdSpec*Req^n;
                end
                yVec(m) = nansum(temp);
            end
        
            %Add noise to make curves distinguishable
            if j == 1
                noiseMag = 13;
            else
                noiseMag = 0.04;
            end
            yVec = yVec + noiseMag*rand(1,26);
        
            %Plot curves per IgG
            plot(xVec,yVec,[color 'x-']);
            hold on
        end
        %Label axes and title graph
        xlabel('Valency');
        ylabel('Number of Ligand Bound');
        if j == 1
            title([name '--Realistic']);
        else
            title([name '--Our Values']);
        end
        %New graph
        hold off
        %Save figure
        if j == 1
            savefig([name '--Realistic']);
        else
            savefig([name '--Our Values']);
        end
    end
end