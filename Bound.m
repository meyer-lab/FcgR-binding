function [ C ] = Bound( r, kx, kd_spec, tnpbsa, v )
    %Granted a receptor expression level r, a constant kx, the specific Kd
    %value of the pertinent receptor-immunoglobulin combination kd_spec,
    %the molarity of TNP-X-BSA used by Lux et al. (see Figure 2), and
    %avidity v, the number of immune complexes bound to a cell should be
    %as follows, according to the model from Stone et al.:
    %
    %   The sum from 1 to v of C_i = v!/((v-i)!*i!)*10^(kx*(i-1))*(tnpbsa/kd_spec)*r^i
    
    % j = 1
    C = v*(tnpbsa/kd_spec)*r;
    
    for j = 2:v
        C = C + nchoosek(v,j)*10^(kx*(j-1))*(tnpbsa/kd_spec)*r^j;
    end
end