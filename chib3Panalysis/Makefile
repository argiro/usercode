#Makefile
#Will define compiler and correct architecture (ARCH, ROOTCFLAGS,ROOTLDFLAGS,ROOTLIBS,ROOTCINT,CXX,CXXFLAGS,LD,LDFLAGS,LIBS,GLIBS, etc.).
#Also defines sufixes: ObjSuf = (o or obj), ExeSuf = (nothing for linux, .exe for windows), DllSuf = (a or so or dylib or dll, etc.), SrcSuf = cxx, OutPutOpt = -o

RC := root-config

include $(ROOTSYS)/etc/Makefile.arch
ROOLIBS = -lRooFit -lRooFitCore

FITO      = yFit3S.$(ObjSuf)
FITS      = yFit3S.$(SrcSuf)
FIT       = yFit3S.x

OBJS      = $(FITO)
PROGRAMS  = $(FIT)

all: $(PROGRAMS)

$(FIT): $(FITO)
	$(LD) $(LDFLAGS) $^ $(LIBS) $(ROOLIBS) $(OutPutOpt)$@
	@echo "$@ done"

clean:
	@rm -f $(OBJS) core

distclean: clean
	@rm -f $(PROGRAMS)

