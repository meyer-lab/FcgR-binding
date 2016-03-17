function [J] = Error26( R )

    [kd, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();

    %Create a figure for the molarity of TNP-X-BSA in the solution into which 
    %the CHO cells were placed (see Lux et al. 2013, Figure 2). The molecular
    %weight of bovine serum albumin is 66463 Da, and the contration of
    %TNP-X-BSA in the solution described in Figure 2 is 5 micrograms per
    %milliliter
    tnpbsa = 1/66463 * 1e-6 * 5 * 1e3;

    %Finding receptor expression and "K_x" by means of minimizing error 
    %functions. I have created error functions Error and Error2 as error 
    %functions for this model against with data in mfiAdjMean4 and 
    %mfiAdjMean26, respectively. The error functions we desire are too complex
    %to write in as anonymous functions in MATLAB; therefore, I wrote them in
    %the files Error.m and Error2.m.
    %We use the MATLAB function fmincon to find the values of R, a six-
    %dimensional vector, and kx, a seventh element appended to the six-
    %dimensional vector R, which yield the minimum value of Error. Essentially,
    %fmincon returns a 7-dimensional vector R, the first six elements being the 
    %calculated expression levels of FcgRIA, FcgRIIA-Arg, FcgRIIA-His, FcgRIIB,
    %FcgRIIIA-Phe, and FcgRIIIA-Val and the last element being a constant kx
    %s.t. 10^kx = K_x yields the best fit to the data using this model.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    temp = zeros(1,96);
    
    for j = 1:6
        for k = 1:4
            for l = 1:4
                temp(16*j+4*k+l-20) = nchoosek(10,l)*10^(R(7)*(l-1))*(tnpbsa/kd(j,k))*R(j)^l;
            end
        end
    end
    
    temp2 = zeros(1,24);
    for j = 1:24
        temp2(j) = nansum(temp((4*j-3):(4*j)));
    end
    
    error = zeros(1,96);
    for j = 1:6
        for k = 1:4
            for l = 1:4
                error(16*j+4*(k)+l-20) = (temp2(4*j+k-4) - mfiAdjMean26((4*j+k-4),l))^2;
            end
        end
    end
    
    J = nansum(error);
end

