count = 0;
for j = 1:700
    if (mod(j,2) == 0) || (mod(j,5) == 0) || (mod(j,7) == 0)
        count = count+1;
    end
end
disp(count)