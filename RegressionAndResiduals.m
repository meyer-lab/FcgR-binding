clc; clear;

%Load the mean fluorecent intensities provided by Lux's lab and affinities
[kd, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData();

%Create a figure for the molarity of TNP-X-BSA in the solution into which 
%the CHO cells were placed (see Lux et al. 2013, Figure 2). The molecular
%weight of bovine serum albumin is 66463 Da, and the contration of
%TNP-X-BSA in the solution described in Figure 2 is 5 micrograms per
%milliliter
tnpbsa = 1/66463 * 1e-6 * 5 * 1e3;

%Let use a model for receptor binding of the form:
%                   
% [C_i] = v!/((v - i)! * i!) * (K_x)^(i-1) * [L]_0/K_d * [R]^i 
% (Stone et al.)
%
%"v" is the valency of the TNP-X-BSA, and we are going to assume the
%valency is 10 for both TNP-4-BSA and TNP-26-BSA. "i" ranges from 1 to 4,
%and "K_d" is the element of matrix kd that is pertinent to the
%combination of receptor flavor and IgG flavor.
%
%Finding receptor expression and "K_x" by means of minimizing error 
%functions. I have created Error and Error2 as error 
%functions for this model against data in mfiAdjMean4 and 
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

R1 = fmincon(@(x) Error4(x),ones(7,1),[],[],[],[],zeros(7,1),(1e6*ones(7,1)));
R2 = fmincon(@(x) Error26(x),ones(7,1),[],[],[],[],zeros(7,1),(1e6*ones(7,1)));

%Saving R1 and R2 for use in later weeks:
%save R1; save R2

%[R1 R2] is approximately equal to:
%
%       [0.0018    0.0009
%        0.2987    0.3411
%        0.3362    0.3469
%        0.3783    0.4602
%        0.2597    0.2863
%        0.0258    0.0225
%        0.2504    0.2510]
%
%Remember that R1(7) and R2(7) are kx s.t. K_x = 10^kx.

%Using these estimates R1 and R2, the MFI we would expect per TNP-X-BSA per
%flavor of receptor per flavor of immunoglobulin per replicate per (mfiExp)
%is as follows:

%For TNP-4-BSA:
mfiExp4 = zeros(24,4);
tempSub = zeros(1,4);
for j = 1:6
    for k = 1:4
        for l = 1:4
            for m = 1:4
                tempSub(m) = nchoosek(10,m)*10^(R1(7)*(m-1))*(tnpbsa/kd(j,k))*R1(j)^m;
            end
            mfiExp4((4*(j)+k-4),l) = nansum(tempSub);
        end
    end
end

%For TNP-26-BSA:
mfiExp26 = zeros(24,4);
tempSub = zeros(1,4);
for j = 1:6
    for k = 1:4
        for l = 1:4
            for m = 1:4
                tempSub(m) = nchoosek(10,m)*10^(R2(7)*(m-1))*(tnpbsa/kd(j,k))*R2(j)^m;
            end
            mfiExp26((4*(j)+k-4),l) = nansum(tempSub);
        end
    end
end

%Residuals:
mfiDiff4 = mfiExp4 - mfiAdjMean4;
mfiDiff26 = mfiExp26 - mfiAdjMean26;

%Saving these matrices as .csv files
%csvwrite('MFIResiduals4.csv',mfiDiff4)
%csvwrite('MIFResiduals26.csv',mfiDiff26)

%See a bar graph of the elements of mfiDiff against their indices:

%bar3(mfiDiff4)
%title('MFI Residuals TNP-4-BSA')
%hold on
%figure
%bar3(mfiDiff26)
%title('MFI Residuals TNP-26-BSA')