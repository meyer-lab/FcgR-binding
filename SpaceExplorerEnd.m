clear; clc;

load('SpaceExplorerApp1Data.mat')
test = 1;
while test
    prompt = input('Input cutoff order of magnitude:\n');
    cutoff = prompt;
    test2 = 1;
    n = 1;
    while test2
        eval(['temp = cutoff < lnstruct.a' num2str(n) ';'])
        if ~temp
            test2 = 0;
        else
            n = n+1;
        end
    end
    
    disp(['Their are ' num2str(n) ' desired optima.'])
    pause(3)
    prompt = input(['Run script "SpaceExplorerEnd"?\n\n'...
        'Input "pls" to proceed. Else, input any string;\n'...
        'be sure to remember single quotes:\n\n']);
    if prompt ~= 'pls'
        test = 0;
    end
end