@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2016a
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2016a\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=PROPRND_mex
set MEX_NAME=PROPRND_mex
set MEX_EXT=.mexw64
call "C:\PROGRA~1\MATLAB\R2016a\sys\lcc64\lcc64\mex\lcc64opts.bat"
echo # Make settings for PROPRND > PROPRND_mex.mki
echo COMPILER=%COMPILER%>> PROPRND_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> PROPRND_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> PROPRND_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> PROPRND_mex.mki
echo LINKER=%LINKER%>> PROPRND_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> PROPRND_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> PROPRND_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> PROPRND_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> PROPRND_mex.mki
echo BORLAND=%BORLAND%>> PROPRND_mex.mki
echo OMPFLAGS= >> PROPRND_mex.mki
echo OMPLINKFLAGS= >> PROPRND_mex.mki
echo EMC_COMPILER=lcc64>> PROPRND_mex.mki
echo EMC_CONFIG=optim>> PROPRND_mex.mki
"C:\Program Files\MATLAB\R2016a\bin\win64\gmake" -B -f PROPRND_mex.mk
