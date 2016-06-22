@echo off
set MATLAB=C:\PROGRA~1\MATLAB\R2015b
set MATLAB_ARCH=win64
set MATLAB_BIN="C:\Program Files\MATLAB\R2015b\bin"
set ENTRYPOINT=mexFunction
set OUTDIR=.\
set LIB_NAME=PDF_mex
set MEX_NAME=PDF_mex
set MEX_EXT=.mexw64
call "C:\PROGRA~1\MATLAB\R2015b\sys\lcc64\lcc64\mex\lcc64opts.bat"
echo # Make settings for PDF > PDF_mex.mki
echo COMPILER=%COMPILER%>> PDF_mex.mki
echo COMPFLAGS=%COMPFLAGS%>> PDF_mex.mki
echo OPTIMFLAGS=%OPTIMFLAGS%>> PDF_mex.mki
echo DEBUGFLAGS=%DEBUGFLAGS%>> PDF_mex.mki
echo LINKER=%LINKER%>> PDF_mex.mki
echo LINKFLAGS=%LINKFLAGS%>> PDF_mex.mki
echo LINKOPTIMFLAGS=%LINKOPTIMFLAGS%>> PDF_mex.mki
echo LINKDEBUGFLAGS=%LINKDEBUGFLAGS%>> PDF_mex.mki
echo MATLAB_ARCH=%MATLAB_ARCH%>> PDF_mex.mki
echo BORLAND=%BORLAND%>> PDF_mex.mki
echo OMPFLAGS= >> PDF_mex.mki
echo OMPLINKFLAGS= >> PDF_mex.mki
echo EMC_COMPILER=lcc64>> PDF_mex.mki
echo EMC_CONFIG=optim>> PDF_mex.mki
"C:\Program Files\MATLAB\R2015b\bin\win64\gmake" -B -f PDF_mex.mk
