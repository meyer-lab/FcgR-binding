Lvec = -15:0.5:-5;
Kxvec = -20:0.5:0;
vvec = 1:1:30;
Kdvec = -12:0.5:-1;

lengthL = length(Lvec);
lengthKx = length(Kxvec);
lengthv = length(vvec);
lengthKd = length(Kdvec);

ordmagdiffL = zeros(lengthL,lengthKx,lengthv,lengthKd,lengthKd);
ordmagdiffRm = ordmagdiffL;

for j = 1:lengthL
    L = Lvec(j);
    for k = 1:lengthKx
        Kx = Kxvec(k);
        for l = 1:lengthv
            v = vvec(j);
            for m = 1:lengthKd
                Kd1 = Kdvec(m);
                for n = lengthKd
                    Kd2 = Kdvec(n);
                    [L1,Rmulti1] = StoneAlt(Kd1,v,Kx,L);
                    [L2,Rmulti2] = StoneAlt(Kd2,v,Kx,L);
                    ordmagdiffL(j,k,l,m,n) = log10(L1/L2);
                    ordmagdiffRm(j,k,l,m,n) = log10(Rmulti1/Rmulti2);
                end
            end
        end
    end
end

save('forGUI.mat','ordmagdiffL','ordmagdiffRm','lengthL','lengthKx','lengthv','lengthKd')