function L = StoneSolver(Rtot,Kx,v,Kd,L0,biCoefMat)    
    %Using the information given, finds the sum L presented in Equation 7
    %in Stone. In this context, all inputs save biCoefMat are scalars.
    
    %Solve for Req, as described in Equation 2 in Stone
    Req = ReqFuncSolver(Rtot, Kd, L0, v, Kx);
    %Check for error output from ReqFuncSolver
    if Req == 1000
        L = -1;
        return
    end
    %Convert from logarithmic scale
    Req = 10^Req;
    
    L = sum(L0/Kd*(biCoefMat(1:v,v)'.*(Kx.^([1:v]-1))).*Req.^[1:v]);
end