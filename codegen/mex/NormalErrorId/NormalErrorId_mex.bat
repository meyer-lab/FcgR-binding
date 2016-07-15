@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2015b
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2015b\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=NormalErrorId_mex
set MEX_NAME=NormalErrorId_mex
set MEX_EXT=.mexw64
call "C:\PROGRA~1\MATLAB\R2015b\sys\lcc64\lcc64\mex\lcc64opts.bat"
echo # Make settings for NormalErrorId > NormalErrorId_mex.mki
echo COMPILER=%COMPILER%>> NormalErrorId_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> NormalErrorId_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> NormalErrorId_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> NormalErrorId_mex.mki
echo LINKER=%LINKER%>> NormalErrorId_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> NormalErrorId_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> NormalErrorId_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> NormalErrorId_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> NormalErrorId_mex.mki
echo BORLAND=%BORLAND%>> NormalErrorId_mex.mki
echo OMPFLAGS= >> NormalErrorId_mex.mki
echo OMPLINKFLAGS= >> NormalErrorId_mex.mki
echo EMC_COMPILER=lcc64>> NormalErrorId_mex.mki
echo EMC_CONFIG=optim>> NormalErrorId_mex.mki
"C:\Program Files\MATLAB\R2015b\bin\win64\gmake" -B -f NormalErrorId_mex.mk
