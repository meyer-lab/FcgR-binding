%Load collected Kd values
load 'kd.mat'

%Load molar concentration of TNP-X-BSA
load 'tnpbsa.mat'

%Load number of receptors per flavor of Fcgamma calculated using fmincon
load 'Rcalc.mat'

%Load MFIs given by Lux (recorded minus background)
load 'mfiAdj.mat'

%Create matrix of expected expression levels based in our modeling :p:p:p:p:p
a = zeros(6,4);
for j = 1:6
    for k = 1:4
        if [j,k] == [1,2]
            a(j,k) = NaN
        else
            a(j,k) = (Rcalc(j)*tnpbsa)/(tnpbsa + kd(j,k));
        end
    end
end

mfiExpRcalc = a