@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2016a
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2016a\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=NormalError2_mex
set MEX_NAME=NormalError2_mex
set MEX_EXT=.mexw64
call "C:\PROGRA~1\MATLAB\R2016a\sys\lcc64\lcc64\mex\lcc64opts.bat"
echo # Make settings for NormalError2 > NormalError2_mex.mki
echo COMPILER=%COMPILER%>> NormalError2_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> NormalError2_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> NormalError2_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> NormalError2_mex.mki
echo LINKER=%LINKER%>> NormalError2_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> NormalError2_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> NormalError2_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> NormalError2_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> NormalError2_mex.mki
echo BORLAND=%BORLAND%>> NormalError2_mex.mki
echo OMPFLAGS= >> NormalError2_mex.mki
echo OMPLINKFLAGS= >> NormalError2_mex.mki
echo EMC_COMPILER=lcc64>> NormalError2_mex.mki
echo EMC_CONFIG=optim>> NormalError2_mex.mki
"C:\Program Files\MATLAB\R2016a\bin\win64\gmake" -B -f NormalError2_mex.mk
