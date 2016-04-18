function [ error ] = Error2(RtotMat, Req, L, kx, v, kd)
    error = nansum(nansum((RtotMat-Req.*(1+(v*L./kd).*(1+kx*Req).^(v-1))).^2));
end    