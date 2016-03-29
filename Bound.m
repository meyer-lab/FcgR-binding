function [ C ] = Bound( r, kd_spec, v, CoefMat )
    %Granted a receptor expression level r, the specific Kd
    %value of the pertinent receptor-immunoglobulin combination kd_spec,
    %the molarity of TNP-X-BSA used by Lux et al. (see Figure 2), valency v,
    %and a coefficient of the form:
    %v!/((v-i)!*i!)*10^(kx+i-1)*tnpbsa (many such coefficients being
    %contained in the matrix CoefMat), the number of immune complexes bound
    %to a cell should be as follows, according to the model from Stone et al.:
    %
    %   The sum from 1 to v of C_i = v!/((v-i)!*i!)*10^(kx*(i-1))*(tnpbsa/kd_spec)*r^i
    
    rKdVec = (r.^(1:v))/kd_spec;

    C = rKdVec*CoefMat(1:v,v);
end