1) First create a file named LinkDef.h with the following:
 
#include "RooDoubleCB.h"
#ifdef __CINT__
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclasses;
#pragma link C++ class RooDoubleCB+;
#endif /* __CINT__ */
 
2) Create the root dictionary for the header of the class and LinkDef:
 
rootcint -f dictDoubleCB.cxx -c RooDoubleCB.h LinkDef.h
 
2bis) in case of compilation on CMSSW env where roofit is installed as a separate sw from ROOT the command is the following:
 
rootcint -f dictDoubleCB.cxx -c -I$ROOFITSYS/include My_double_CB.h LinkDef.h
 
N.B. The pickyness of rootcint requires NO spaces between the -I and the include dir!!!
 
3) Compile everything into a single shared object that can be included  later to fit with:
 
g++  -shared -o  myDoubleCB.so `root-config --ldflags --cflags --glibs`  -lRooFit -lRooFitCore 
-lRooStats -lMinuit -I `root-config --incdir`  myDoubleCB.cxx dictDoubleCB.cxx

3bis) Again, on CMSSW the command is a little different, in order to include correctly roofit:
 
g++ -fPIC -shared -o myDoubleCB.so `root-config --ldflags --cflags --glibs` -L $ROOFITSYS/lib -lRooFit -lRooFitCore -lRooStats -lMinuit -I `root-config --incdir` -I $ROOFITSYS/include myDoubleCB.cxx dictDoubleCB.cxx
