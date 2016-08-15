@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2016a
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2016a\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=NormalErrorCoef_mex
set MEX_NAME=NormalErrorCoef_mex
set MEX_EXT=.mexw64
call "C:\PROGRA~1\MATLAB\R2016a\sys\lcc64\lcc64\mex\lcc64opts.bat"
echo # Make settings for NormalErrorCoef > NormalErrorCoef_mex.mki
echo COMPILER=%COMPILER%>> NormalErrorCoef_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> NormalErrorCoef_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> NormalErrorCoef_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> NormalErrorCoef_mex.mki
echo LINKER=%LINKER%>> NormalErrorCoef_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> NormalErrorCoef_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> NormalErrorCoef_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> NormalErrorCoef_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> NormalErrorCoef_mex.mki
echo BORLAND=%BORLAND%>> NormalErrorCoef_mex.mki
echo OMPFLAGS= >> NormalErrorCoef_mex.mki
echo OMPLINKFLAGS= >> NormalErrorCoef_mex.mki
echo EMC_COMPILER=lcc64>> NormalErrorCoef_mex.mki
echo EMC_CONFIG=optim>> NormalErrorCoef_mex.mki
"C:\Program Files\MATLAB\R2016a\bin\win64\gmake" -B -f NormalErrorCoef_mex.mk
