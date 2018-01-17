from ROOT import RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooGenericPdf, RooCmdArg, RooStats
from ROOT import RooCBShape, RooAddPdf, RooArgList, RooPlot, RooDataHist, RooFitResult, RooAbsPdf
from ROOT import RooFit, gROOT, TStyle, gStyle, gPad
from ROOT import TFile, TCanvas, TH1F, TGraphErrors, TPad, TLegend, TPaveText, TMultiGraph, TGraphErrors, TMath
from ROOT import TH1F, TTree, RooHistPdf,RooCategory,RooSimultaneous
import ROOT
import sys



def makeDataSet(channel) :
    
    inputfile_name = "chibds-s-kinfit-corr.root"
    if channel == '2S':
        inputfile_name = "chibds-s-kinfit-2S-corr.root"
    if channel == '3S':
        inputfile_name = "chibds-s-kinfit-3S-corr.root"


    inputfile = TFile(inputfile_name)

    
    dataSet = inputfile.Get('chicds')

#    cuts1S="Y1S_nsigma < 2.5 && photon_pt > 0.5 && abs(photon_eta) < 1.4 && dimuon_pt > 9.5 && abs(dimuon_rapidity) < 1.25  &&  abs(dz) < 0.1 && invm1S> 10.35 && invm1S<10.8"
    
#    cuts2S = "photon_pt > 0.8 && dimuon_pt>9.5   && abs(dimuon_rapidity) < 1.25 && Y2S_nsigma < 2.5 && abs(dz) < 0.1 && abs(photon_eta) < 1.4"


#my last

#    cuts1S = "pt_gamma > 1.0 && abs(eta_gamma) < 1. && abs(y_mumu) < 1.25 && psi1S_nsigma < 2.5 && abs(dz) < 0.1 && probFit1S>0.1"
    

#    cuts2S = "pt_gamma > 0.75 && abs(eta_gamma) < 1. && abs(y_mumu) < 1.25 && psi2S_nsigma < 2.5 && abs(dz) < 0.1 && probFit2S>0.1"




#    cuts3S = "pt_gamma > 0.0" +                    \
#             "&& pt_mumu > 9.5"                    \
#             "&& abs(eta_gamma) < 1.4" +           \
#             "&& abs(y_mumu) < 1.25 " +            \
#             "&& abs(dz) < 0.1" +                  \
#             "&& probFit3S>0.1"
#             "&& psi3S_nsigma < 2.5 " +           \


#Giulia ottimizzati

    cuts1S='pt_gamma >1.0 && pt_mumu>9.5 && abs(y_mumu)<1.4 && abs(dz)<0.5 && probFit1S>0.01 && rho_conv>1.5 && psi1S_nsigma<0.0025'

    cuts2S='pt_gamma >1.0 && pt_mumu>10 && abs(y_mumu)<1.4 && abs(dz)<0.5 && probFit2S>0.01 && rho_conv>1.5 && psi2S_nsigma<0.0025'  

    cuts3S='pt_gamma >0.5 && pt_mumu>10.5 && abs(y_mumu)<1.1 && abs(dz)<0.5 && probFit3S>0.01 && rho_conv>1.5 && psi3S_nsigma<0.0025'
    
    cuts = cuts1S
    if channel =='2S': cuts = cuts2S
    if channel =='3S': cuts = cuts3S
        
    rds_cutted = dataSet.reduce( RooFit.Cut(cuts) )
    
    return rds_cutted



dataset1S = makeDataSet('1S')
dataset2S = makeDataSet('2S')
dataset3S = makeDataSet('3S')




mass_chib3s =  10.5103 # from PES uncorrected mass measurement
deltaM3s    =  0.0105   #  MeV theoretical expectations
ratio213s   =  0.45     # same as chic2/chic1 and chib2/chib1
deltaM_v3s  = RooRealVar('deltaM3s','#Delta_{m}',deltaM3s)
ratio21_v3s = RooRealVar('ratio213s','r_{21}',ratio213s)


x = RooRealVar("Qvalue","Qvalue",10.35,10.8)
x.setBins(90)

sigma_1S = RooRealVar("sigma_1S","#sigma(3P1)1S", 0.014)
sigma_2S = RooRealVar("sigma_2S","#sigma(3P1)2S", 0.010)


alpha_1S  = RooRealVar("alpha_1S","#alpha(3P)1S", 0.6)
alpha_2S  = RooRealVar("alpha_2S","#alpha(3P)2S", 0.6)

n_1S    = RooRealVar("n_1S","n(3P1)1S", 2.5)
n_2S    = RooRealVar("n_2S","n(3P1)2S", 2.5)


rawmass = RooRealVar('rm','rm',10.5,10.4,10.6)
mass3P_1S2 =RooFormulaVar("m1","(@0+@1)",RooArgList(rawmass,deltaM_v3s)) 
mass3P_2S2 =RooFormulaVar("m2","(@0+@1)",RooArgList(rawmass,deltaM_v3s))

mass3P_3S2 =RooFormulaVar("m3","(@0+@1)",RooArgList(rawmass,deltaM_v3s)) 

signal1S_1 = RooCBShape('signal1S1','s1S1',x,rawmass,sigma_1S,alpha_1S,n_1S)
signal1S_2 = RooCBShape('signal1S2','s1S2',x,mass3P_1S2,sigma_1S,alpha_1S,n_1S)



signal2S_1 = RooCBShape('signal2S1','s2S1',x,rawmass,sigma_2S,alpha_2S,n_2S)
signal2S_2 = RooCBShape('signal2S2','s2S1',x,mass3P_2S2,sigma_2S,alpha_2S,n_2S)


#3S parameters
 
# the following numbers are from an old 3P gun simulation
# that needs to be re-done
    
sigma13s    =  0.003#0.0031 
sigma23s    =  0.003#0.0035
    
alpha13s    =  0.95
alpha23s    =  1.12

n3s         =  2.5  


#mass1_v3s   = RooRealVar('mchi13s','m_{#chi1}',mass_chib3s,mass_chib3s-0.1 , mass_chib3s+0.1 )
#deltaM_v3s  = RooRealVar('deltaM3s','#Delta_{m}',deltaM3s,0.005,0.015)


sigma1_v3s  = RooRealVar('sigma13s','#sigma_1',sigma13s)
sigma2_v3s  = RooRealVar('sigma23s','#sigma_2',sigma23s)

alpha1_v3s  = RooRealVar('alpha13s','#alpha_1',alpha13s)
alpha2_v3s  = RooRealVar('alpha23s','#alpha_2',alpha23s)

n_v3s       = RooRealVar('n3s','n',n3s)


chib13s = RooCBShape('chib13s','chib1',x,rawmass,sigma1_v3s,alpha1_v3s,n_v3s)
chib23s = RooCBShape('chib23s','chib2',x,mass3P_3S2,sigma2_v3s,alpha2_v3s,n_v3s)





#background parameters

q01S_Start = 9.62
alphabkg1S =    RooRealVar("#alpha1S","#alpha1S",1.5,0.2,10)
beta =     RooRealVar("#beta1S","#beta1S",-2.5,-7.,0.)
q01S   =      RooRealVar("q01S","q01S",q01S_Start)
delta1S =     RooFormulaVar("delta1S","TMath::Abs(@0-@1)",RooArgList(x,q01S))
b11S =        RooFormulaVar("b11S","@0*(@1-@2)",RooArgList(beta,x,q01S))
signum11S =   RooFormulaVar( "signum11S","( TMath::Sign( -1.,@0-@1 )+1 )/2.", RooArgList(x,q01S) )

background1S = RooGenericPdf("background","Background", "signum11S*pow(delta1S,#alpha1S)*exp(b11S)", RooArgList(signum11S,delta1S,alphabkg1S,b11S) )


q02S_Start = 10.0
alphabkg2S = RooRealVar("#alpha2S","#alpha2S",1.5,0.2,3.5)
beta2S =     RooRealVar("#beta2S","#beta2S",-2.5,-7.,0.)
q02S   =     RooRealVar("q02S","q02S",q02S_Start,q02S_Start-0.05,q02S_Start+0.05)
delta2S =     RooFormulaVar("delta2S","TMath::Abs(@0-@1)",RooArgList(x,q02S))
b12S =        RooFormulaVar("b12S","@0*(@1-@2)",RooArgList(beta2S,x,q02S))
signum12S =   RooFormulaVar( "signum12S","( TMath::Sign( -1.,@0-@1 )+1 )/2.", RooArgList(x,q02S) )

background2S = RooGenericPdf("background","Background", "signum12S*pow(delta2S,#alpha2S)*exp(b12S)", RooArgList(signum12S,delta2S,alphabkg2S,b12S) )



# define background
q01S_Start3s = 10.4
alpha3s =    RooRealVar("#alpha3s","#alpha",1.5,0.2,3.5)
beta3s =     RooRealVar("#beta3s","#beta",-2.5,-7.,0.)
#q0   =      RooRealVar("q0","q0",q01S_Start,q01S_Start-0.05,q01S_Start+0.05)
q03s   =      RooRealVar("q03s","q0",q01S_Start3s)
delta3s =     RooFormulaVar("delta3s","TMath::Abs(@0-@1)",RooArgList(x,q03s))
b13s =        RooFormulaVar("b13s","@0*(@1-@2)",RooArgList(beta3s,x,q03s))
signum13s =   RooFormulaVar( "signum13s","( TMath::Sign( -1.,@0-@1 )+1 )/2.", RooArgList(x,q03s) )


background3s = RooGenericPdf("background3s","Background", "signum13s*pow(delta3s,#alpha3s)*exp(b13s)", RooArgList(signum13s,delta3s,alpha3s,b13s) )


nsig1S1 = RooRealVar('nsig1S1','nsig1S1',200,0,1000)
nsig1S2 = RooFormulaVar('nsig1S2','@0*@1',RooArgList(nsig1S1,ratio21_v3s))

nsig2S1 = RooRealVar('nsig2S1','nsig2S1',200,0,1000)
nsig2S2 = RooFormulaVar('nsig2S2','@0*@1',RooArgList(nsig2S1,ratio21_v3s))

nbck1S = RooRealVar('nbck1S','nbck1S',1000,0,100000)

nsig2S = RooRealVar('nsig2S','nsig2S',60,0,500)
nbck2S = RooRealVar('nbck2S','nbck2S',1000,0,100000)




model1S =  RooAddPdf('model1S','model1S',RooArgList(signal1S_1,signal1S_2,background1S),RooArgList(nsig1S1,nsig1S2,nbck1S))
model2S =  RooAddPdf('model2S','model2S',RooArgList(signal2S_1,signal2S_2,background2S),RooArgList(nsig2S1,nsig2S2,nbck2S))


n_evts_1_3s = RooRealVar('N_{3P_{1}}','N_{3P_{1}}',50,10,1000)
n_evts_2_3s = RooFormulaVar('N_{3P_{2}}','@0*@1',RooArgList(n_evts_1_3s,ratio21_v3s))
n_bck3s    = RooRealVar('nbkg3s','n_{bkg}',500,0,100000)


model3S = RooAddPdf('model3S', 'model3S', RooArgList(chib13s,chib23s,background3s),RooArgList(n_evts_1_3s,n_evts_2_3s,n_bck3s))


# start simultaneous fit



sample= RooCategory('sample','sample')
sample.defineType('b1')
sample.defineType('b2') 
sample.defineType('b3') 
  
combData= RooDataSet('combData','combined data',RooArgSet( x),
                     RooFit.Index(sample),
                     RooFit.Import('b1',dataset1S),
                     RooFit.Import('b2',dataset2S),
                     RooFit.Import('b3',dataset3S),
                     )

#model1S,model2S = definemodel(x)

simPdf = RooSimultaneous("simPdf","simultaneous pdf",sample) ;

simPdf.addPdf(model1S,'b1') 
simPdf.addPdf(model2S,'b2')
simPdf.addPdf(model3S,'b3')

fitregion = x.setRange('fitregion',10.35,10.8)
fitregion_1S = x.setRange('fitregion_1S',10.35,10.8)
fitregion_2S = x.setRange('fitregion_2S',10.35,10.8)
fitregion_3S = x.setRange('fitregion_3S',10.35,10.8)

#simPdf.fitTo(combData,RooFit.Save(), RooFit.Range('fitregion'),RooFit.SplitRange())


simPdf.fitTo(combData,RooFit.Save())

#plotting
frame1 = x.frame()
combData.plotOn(frame1,
                RooFit.Cut("sample==sample::b1"),
                RooFit.MarkerSize(0.7))
simPdf.plotOn(frame1, RooFit.Slice(sample,'b1'),
              RooFit.ProjWData(RooArgSet(sample),combData),
              RooFit.LineWidth(2))

c1 = TCanvas('c1','c1')
frame1.Draw()

frame2 = x.frame()
combData.plotOn(frame2,
                RooFit.Cut("sample==sample::b2"),
                RooFit.MarkerSize(0.7))
simPdf.plotOn(frame2, RooFit.Slice(sample,'b2'),
              RooFit.ProjWData(RooArgSet(sample),combData),
              RooFit.LineWidth(2))

dataset2S.plotOn(frame2)

c2 = TCanvas('c2','c2')
frame2.Draw()

frame3 = x.frame()
combData.plotOn(frame3,
                RooFit.Cut("sample==sample::b3"),
                RooFit.MarkerSize(0.7))
simPdf.plotOn(frame3, RooFit.Slice(sample,'b3'),
              RooFit.ProjWData(RooArgSet(sample),combData),
              RooFit.LineWidth(2))

dataset3S.plotOn(frame3)

c3 = TCanvas('c3','c3')
frame3.Draw()



file = TFile('outSimFit3P-kinfit.root','recreate')
c1.Write()
c2.Write()
c3.Write()




