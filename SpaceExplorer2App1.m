clear;clc;

load('SpaceExplorer2Data.mat')

len = (RissL-1)^2*(vissL-1)^2;

SpaceExplorer2App1cell = cell(1,6);
for j = 1:6
    pstruct = struct;
    lnstruct = struct;
    for k = 1:len
        clear current
        high = -inf;
        str = num2str(k);
        for l = 1:len
            temp = lntent{k};
            if ~isempty(temp)
                if temp > high
                    high = temp;
                    current = ptent{k};
                    ind = k;
                end
            end
        end
        eval(['pstruct.a' str ' = current;'])
        eval(['lnstruct.a' str ' = high;'])
        lntent{ind} = [];
    end
    SpaceExplorer2App1cell{j} = {pstruct lnstruct};
end
save('SpaceExplorer2App1Data.mat','SpaceExplorer2App1cell')

disp('All SpaceExplorer scripts complete.')