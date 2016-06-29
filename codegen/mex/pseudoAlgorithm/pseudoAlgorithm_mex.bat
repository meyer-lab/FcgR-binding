@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2015b
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2015b\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=pseudoAlgorithm_mex
set MEX_NAME=pseudoAlgorithm_mex
set MEX_EXT=.mexw64
call "C:\PROGRA~1\MATLAB\R2015b\sys\lcc64\lcc64\mex\lcc64opts.bat"
echo # Make settings for pseudoAlgorithm > pseudoAlgorithm_mex.mki
echo COMPILER=%COMPILER%>> pseudoAlgorithm_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> pseudoAlgorithm_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> pseudoAlgorithm_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> pseudoAlgorithm_mex.mki
echo LINKER=%LINKER%>> pseudoAlgorithm_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> pseudoAlgorithm_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> pseudoAlgorithm_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> pseudoAlgorithm_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> pseudoAlgorithm_mex.mki
echo BORLAND=%BORLAND%>> pseudoAlgorithm_mex.mki
echo OMPFLAGS= >> pseudoAlgorithm_mex.mki
echo OMPLINKFLAGS= >> pseudoAlgorithm_mex.mki
echo EMC_COMPILER=lcc64>> pseudoAlgorithm_mex.mki
echo EMC_CONFIG=optim>> pseudoAlgorithm_mex.mki
"C:\Program Files\MATLAB\R2015b\bin\win64\gmake" -B -f pseudoAlgorithm_mex.mk
