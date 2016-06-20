function output = libfzero(vi, Li, kdi, kx, R) 

    if ~libisloaded('libfzero')
        loadlibrary('libfzero.dylib', 'libfzero.h');
    end
    
    outP = libpointer('doublePtr',zeros(1,numel(kdi)));

    calllib('libfzero','bisectMat',...
        vi, Li, libpointer('doublePtr',kdi), kx, ...
        libpointer('doublePtr',R), numel(kdi), outP);

    output = 10.^(outP.Value);
end

% extern "C" void bisectMat(double vi, double Li, double *kdi, double kx, double *R, int N, double *output); 