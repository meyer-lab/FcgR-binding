clear;

load('SpaceExplorerData.mat')

pstruct = struct;
lnstruct = struct;
len = (RissL-1)^7*(vissL-1)^2;
for j = 1:len
    clear current
    high = -inf;
    str = num2str(j);
    for k = 1:len
        temp = lntent{j};
        if ~isempty(temp)
            if temp > high
                high = temp;
                current = ptent{j};
                ind = j;
            end
        end
    end
    eval(['pstruct.a' str ' = current;'])
    eval(['lnstruct.a' str ' = high;'])
    lntent{ind} = [];
end

save('SpaceExplorerApp1Data.mat','pstruct','lnstruct')

disp('SpaceExplorerApp1 complete.')

% Move on to SpaceExplorer2
SpaceExplorer2;