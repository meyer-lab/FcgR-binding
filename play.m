load('DiffCompare.mat')

temp = [];
for j = 1:6
    for k = 1:6
        if (bigDiffLigand(2,j,k) > 10) && (DiffLigand(2,j,k) < 20)
            temp = [temp [bigDiffLigand(:,j,k);j;k]];
        end
    end
end