function [ C ] = Bound( r, kd_spec, tnpbsa, v, CoefMat )
    %Granted a receptor expression level r, the specific Kd
    %value of the pertinent receptor-immunoglobulin combination kd_spec,
    %the molarity of TNP-X-BSA used by Lux et al. (see Figure 2), valency v,
    %and a coefficient of the form:
    %v!/((v-i)!*i!)*10^(kx+i-1)*tnpbsa (many such coefficients being
    %contained in the matrix CoefMat), the number of immune complexes bound
    %to a cell should be as follows, according to the model from Stone et al.:
    %
    %   The sum from 1 to v of C_i = v!/((v-i)!*i!)*10^(kx*(i-1))*(tnpbsa/kd_spec)*r^i
    
    rKdVec = zeros(1,10);
    for j = 1:10
        rKdVec(j) = r^j;
    end
    rKdVec = rKdVec/kd_spec;
    
    CoefVec = CoefMat(:,v);

    C = rKdVec*CoefVec;
end