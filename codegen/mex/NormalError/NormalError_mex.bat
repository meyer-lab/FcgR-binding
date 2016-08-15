@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2016a
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2016a\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=NormalError_mex
set MEX_NAME=NormalError_mex
set MEX_EXT=.mexw64
call "C:\PROGRA~1\MATLAB\R2016a\sys\lcc64\lcc64\mex\lcc64opts.bat"
echo # Make settings for NormalError > NormalError_mex.mki
echo COMPILER=%COMPILER%>> NormalError_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> NormalError_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> NormalError_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> NormalError_mex.mki
echo LINKER=%LINKER%>> NormalError_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> NormalError_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> NormalError_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> NormalError_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> NormalError_mex.mki
echo BORLAND=%BORLAND%>> NormalError_mex.mki
echo OMPFLAGS= >> NormalError_mex.mki
echo OMPLINKFLAGS= >> NormalError_mex.mki
echo EMC_COMPILER=lcc64>> NormalError_mex.mki
echo EMC_CONFIG=optim>> NormalError_mex.mki
"C:\Program Files\MATLAB\R2016a\bin\win64\gmake" -B -f NormalError_mex.mk
