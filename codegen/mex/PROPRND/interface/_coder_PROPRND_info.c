/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * _coder_PROPRND_info.c
 *
 * Code generation for function '_coder_PROPRND_info'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "PROPRND.h"
#include "_coder_PROPRND_info.h"
#include "PROPRND_data.h"

/* Function Definitions */
mxArray *emlrtMexFcnProperties(void)
{
  mxArray *xResult;
  mxArray *xEntryPoints;
  const char * fldNames[4] = { "Name", "NumberOfInputs", "NumberOfOutputs",
    "ConstantInputs" };

  mxArray *xInputs;
  const char * b_fldNames[4] = { "Version", "ResolvedFunctions", "EntryPoints",
    "CoverageInfo" };

  xEntryPoints = emlrtCreateStructMatrix(1, 1, 4, fldNames);
  xInputs = emlrtCreateLogicalMatrix(1, 15);
  emlrtSetField(xEntryPoints, 0, "Name", mxCreateString("PROPRND"));
  emlrtSetField(xEntryPoints, 0, "NumberOfInputs", mxCreateDoubleScalar(15.0));
  emlrtSetField(xEntryPoints, 0, "NumberOfOutputs", mxCreateDoubleScalar(1.0));
  emlrtSetField(xEntryPoints, 0, "ConstantInputs", xInputs);
  xResult = emlrtCreateStructMatrix(1, 1, 4, b_fldNames);
  emlrtSetField(xResult, 0, "Version", mxCreateString("9.0.0.341360 (R2016a)"));
  emlrtSetField(xResult, 0, "ResolvedFunctions", (mxArray *)
                emlrtMexFcnResolvedFunctionsInfo());
  emlrtSetField(xResult, 0, "EntryPoints", xEntryPoints);
  emlrtSetField(xResult, 0, "CoverageInfo", covrtSerializeInstanceData
                (&emlrtCoverageInstance));
  return xResult;
}

const mxArray *emlrtMexFcnResolvedFunctionsInfo(void)
{
  const mxArray *nameCaptureInfo;
  const char * data[18] = {
    "789ced5dcb6f1b45189fd0b41450a1201e2a2da2e150b5aada4d1afa080748da348d4bd2983469d246553ade1d3723f6a5dd4dea72b23871a804e284382171a3"
    "4280f807ca1f80d4035cf807b8d01bdcd9f17ae3f578e399ecce3e1c8d25cbf9e2f9667fdf6be69ba7c150651ef8af97fdf7ea97001cf03f0ffaefe740f0dadf",
    "a687fcb7d2fe0cfe3f0c0eb5e9cffdb76a991e6a78c197263410085f9a6560139aded2431b0107b996be85b4d63775aca3256ca0392b42cc629f3066225f6d13"
    "e42b67c3ddae19e851227811399e808e1cc331723c8ac871b84daf5dbd7be50365d9458eab18d8839aa14c5b0f4cdd829aab384845b6b9698c9d41e3ef8fa1f3",
    "108d4d8c9e1b1fadc331347eb1367e016a17262e9eaf9d9b1857b5894b505593b0541717aa8b37a6cf1aa11cb30c395ea5e4203432f475c3f395e5ae6f20dd46"
    "4e442fa37dea0b5fd1fa42be2f18386e527c845eabccadb6545a75acfb0e348e1323bacafcd4d2dcd46565f1dce8d805a87896a5d7ac86e28356745c530ce8e9",
    "b0a658b6abf4c811a8a585e75204cf81183c43113c2f6ccbd7fc79e5c89f53c9f93bfa289aff64847f28861f443e9394ff06f4b73704ddf6267406f61e512dc3"
    "b0cc757503a99fba117c5506be77297c84562dcdaf13fb8d946342fd2c762f6f62ddab9837360de460b5c72e71f51ea0ea25b4666dd674c41727ab14ff6a12bd",
    "91f7e99634cae9501c8516e7ac91c2cf668ffffe878c138ef24f417f7b7f0bbaed4de832f53323de03cb83bebf356cc7d4e2f5ce1b07611d22e2c866f07f48f1"
    "137aadc21f46ae073d3708a6166ad2b5a4e857b4532b325e78ca176557561ef51af55c426f411d6bd043d0f31c5cdbf490db91a35f1e35d4fe5fa7be61a0225d",
    "e7e91f96291ccb205dbfaa43f3bed22b482b934ae1ef2f3e33651ec553be6cf666e54def507808dd9337552db7627a3755a84327c60e59e44db728fe5b49f4b4"
    "43de1415275d3f00cefc23e342485ce46d6f565cbc4de121744f5c448322c60e59c4859071f70e7aea52528c3cbbf0ab13322ec4c44591f68ec3b39fc243e8ba",
    "6e59a2fa852683bf42f15792e823d27f22bdbe692a2d09da5a48e537bf2d9f907ecf53be09ca616739af24e795643c7470b0e2e1288583d0543cb8419f12f60a"
    "d9ae4308194fc5c6c1e9408e888e528c9f7f90eb10831507f718384e5138084dc501b46dfd619060cd6c9aaa872db3625675a8a2c8732619cf79857a0ea1ebed",
    "dad637a0a9f91d06cffa4d8daaa796446fb171b2b398a14253f89df3efb88c1b9ef265b77f56fd4ad67996ec5ff6569cb0ec3d08e36dec62b3cec95fbef1b6ff"
    "87d29240c478fb27e9f765cdabe2ed2cc7db72bc5d8678c8a5dfdfc53addaed79737a09386afc9e013dd1eb89e43065ae4f102dafde6d777916cf779ca0fd2fe",
    "0baa9defda9f94959f7f4ce1f818886ad78932ec6dfc09fdfc89f15da17efe58547e55747e53849d8bd847c7ead75628fe95b61eaae915613b78cbefdcc286c0"
    "1e60bf6f1efb754e4c1e55741e93b7bd93b4fb72dfdd8e7e28f7dd71961fb4387893c243687abeb30175dd52f399e759a0f81780a8feb12d861f0965c8438ae6",
    "2f3a0fcacbce2cff7f8bc241e8d8f9feabf773f1ff2ac55f15a797b618a9e6754e3e5b90fe2fc2fff3b2f32403c7210a07a1b16b0653801e39363b40ed3ec983"
    "eab88134dbf2d5a174c991aeddff51b6fb83e5f72c7f3d48e1203476ebd84fa337f2f0f7eb14fff5247ae8f1f700bf80fd0ed2df39cbb3f2fdecd66b3afe3e52",
    "c78eebd57192712af11911fede60f0cf50fc3349f410e3ef29cfcd483fe72c5fb47d2719cfe7cd63b29abf97f9cbdef0f326c8c1ce1ce35641fbd450c39e0a26"
    "6f62f49fc5bcfe12c5bf244e3f11713af7d4c8799c62f39bbcedbdcac0f31e8587d07de2e2867585dcf0126f8f24f1f115837f8de25fcb445f6db1d2df5b74f8",
    "e1b08c13117192f7bcff6ef31c079ada408d7bdbeb5d0437d9d0433e058c7b3ffa5bce6f0ac993f2b2f32c03c71b140e4293fbbeb0bb4eaa5a470dcfc1a68b55"
    "c01e1f84af687d210ed6b9078de2d34092f88f51c876f4c70995364f6afe22f3a4bdd9feefebc2b30fe89698f52dd63cc1358aff1a10716ece479f6e7c2ccfcb",
    "73962fdabeac71f131eaf984eed9b73f6d19109b571d2738c0c533bfc47bfe91d50e64778eab4bac94fb7dc05f1b321e06221e58f9cfebd4f3094dc5038ac641"
    "56f3a3f3148ef9247a88f57b24c0df9bff21b98f7f20fc9dd5fe1fa19e4fe8f8f3bb24e3e9c895d5bd10d99de30ccfed06ba09f1c873bb7bdbffef319e2fef83",
    "90f74194295eca6effacfa93acd7d964bfb2b7e2a4ccf68ec3f33c8587d00e82ba011b998e23849c9febb91fa08d3cfd7da3f21e08cef24d500e3b4f3270bc44"
    "e12034996a0f7d3dac27a9bfb3e27ea7fd8389d70d024544570db69522fdbef8763e6f7b0bc87feaba05bd79ff7f7a44ceace26191c2b30844f5831d31d28f0f",
    "64deb357f39e83141e421b8e86b7b0860671ff04f9fdab107ffbfa80347e53f43d11c2d6ab8bce7f8ab033779e1f5423649ccbd283e8fb7f881e423508b8ffe7"
    "f1d14f643b2fc2dff3b2b3bcf74ddefb26e3a18383150fc7291c848edf4f7dc5326ce861dfa345c4036b1ff56d8aff7612fdf4db47dd1147c4fda0f2bc0167f9",
    "2628475ccc327070dc1be7d71aaff72cf2a4ecee15f3c548bf0ef0bdcc93f8cab3f280b2dd1fc4110726343bf2957a5d20562d3efcf4eb02c2ee712b9a3f6bff"
    "7f0afadb79affeaef17e4a2e4293bdfc9893bf14fdc70ee73570fafee39a332dfb0f11f9535e76669dd31ca170109adea7e4fa11eddd227719dec49fa12947c4",
    "7e3dd6b8e20ec57727897ee2f7a3f48823609d41b5655c0c545c243d9799d4df5972cbf398d2bfb3eadf79f31cf9bbaddbfe22cfa171967f02fadbf911e8b633"
    "a1cb344e88d3b31c17c8714116f1f23f8039fe7f", "" };

  nameCaptureInfo = NULL;
  emlrtNameCaptureMxArrayR2016a(data, 36712U, &nameCaptureInfo);
  return nameCaptureInfo;
}

/* End of code generation (_coder_PROPRND_info.c) */
