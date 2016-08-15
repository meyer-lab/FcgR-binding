@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2016a
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2016a\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=NormalErrorCoef2_mex
set MEX_NAME=NormalErrorCoef2_mex
set MEX_EXT=.mexw64
call setEnv.bat
echo # Make settings for NormalErrorCoef2 > NormalErrorCoef2_mex.mki
echo COMPILER=%COMPILER%>> NormalErrorCoef2_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> NormalErrorCoef2_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> NormalErrorCoef2_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> NormalErrorCoef2_mex.mki
echo LINKER=%LINKER%>> NormalErrorCoef2_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> NormalErrorCoef2_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> NormalErrorCoef2_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> NormalErrorCoef2_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> NormalErrorCoef2_mex.mki
echo BORLAND=%BORLAND%>> NormalErrorCoef2_mex.mki
echo OMPFLAGS=/openmp >> NormalErrorCoef2_mex.mki
echo OMPLINKFLAGS=/nodefaultlib:vcomp /LIBPATH:"C:\PROGRA~1\MATLAB\R2016a\bin\win64" >> NormalErrorCoef2_mex.mki
echo EMC_COMPILER=msvc140>> NormalErrorCoef2_mex.mki
echo EMC_CONFIG=optim>> NormalErrorCoef2_mex.mki
"C:\Program Files\MATLAB\R2016a\bin\win64\gmake" -B -f NormalErrorCoef2_mex.mk
