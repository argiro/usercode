
#
# Fit the Y3S+gamma spetrum
#
# Stefano Argiro', University of Turin and INFN
#

from ROOT import RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooGenericPdf, RooCmdArg, RooStats
from ROOT import RooCBShape, RooAddPdf, RooArgList, RooPlot, RooDataHist, RooFitResult, RooAbsPdf,RooGaussian
from ROOT import RooFit, gROOT, TStyle, gStyle, gPad
from ROOT import TFile, TCanvas, TH1F, TGraphErrors, TPad, TLegend, TPaveText, TMultiGraph, TGraphErrors, TMath
from ROOT import TH1F, TTree, RooHistPdf
import ROOT
import sys

def main() :
    inputfile_name = "/data1/chibdata/collision/v2/2012_AllData_v2.root"

    chibTree_name = "rootuple/chibTree"
    print "Opening file"
    inputfile = TFile.Open(inputfile_name,"READ")
    print "Importing tree"
    tree = TTree()
    inputfile.GetObject(chibTree_name, tree)

    invm1S = RooRealVar("invm1S", "invm1S", 9.5, 11.5)
    invm2S = RooRealVar("invm2S", "invm2S", 9.5, 20.0)
    invm3S = RooRealVar("invm3S", "invm3S", 9.5, 20.0)
    dimuon_mass = RooRealVar("dimuon_mass","dimuon_mass", 8.0, 12.0)
    dimuon_rapidity = RooRealVar("dimuon_rapidity", "dimuon_rapidity", -5.0, 5.0)
    dimuon_pt = RooRealVar("dimuon_pt","dimuon_pt", 0.0, 100.0)
    photon_eta = RooRealVar("photon_eta","photon_eta", -5.0, 5.0)
    photon_pt = RooRealVar("photon_pt","photon_pt", 0.0, 100.0)
    ctpv = RooRealVar("ctpv","ctpv", -5.0, 5.0)
    ctpv_error = RooRealVar("ctpv_err","ctpv_err", -5.0, 5.0)
    pi0_abs_mass = RooRealVar("pi0_abs_mass","pi0_abs_mass", 0.0, 2.0)
    Y1S_nsigma = RooRealVar("Y1S_nsigma","Y1S_nsigma",0.0,30.0)
    Y2S_nsigma = RooRealVar("Y2S_nsigma","Y2S_nsigma",0.0,30.0)
    Y3S_nsigma = RooRealVar("Y3S_nsigma","Y3S_nsigma",0.0,35.0)
    conv_vertex = RooRealVar("conv_vertex", "conv_vertex", 0.0, 70.0)
    dz = RooRealVar("dz","dz", -50.0, 50.0)


    print "Assigning argset"
    dataArgSet = RooArgSet(invm1S, invm2S, invm3S, dimuon_mass, dimuon_rapidity, dimuon_pt, photon_eta, photon_pt, ctpv)
    dataArgSet.add( ctpv_error )
    dataArgSet.add( pi0_abs_mass )
    dataArgSet.add( Y1S_nsigma )
    dataArgSet.add( Y2S_nsigma )
    dataArgSet.add( Y3S_nsigma )
    dataArgSet.add( conv_vertex )
    dataArgSet.add( dz )

    print "Creating DataSet"
    dataSet = RooDataSet("chibds","Chib RooDataSet", tree, dataArgSet)


    # Selection
    cuts = "photon_pt > 0.0" +                   \
           "&&dimuon_pt > 9.5"                   \
           "&& abs(photon_eta) < 1.4" +          \
           "&& abs(dimuon_rapidity) < 1.25 " +   \
           "&& Y3S_nsigma < 2.5 " +              \
           "&& abs(dz) < 0.1"

    rds_cutted = dataSet.reduce( RooFit.Cut(cuts) )

    dofit(rds_cutted, "Chib_fit_2012_3S")

def dofit(roodataset, hname):
  
    mass_chib =  10.5103 # from PES uncorrected mass measurement

    deltaM    =  0.0105   #  MeV theoretical expectations
    ratio21   =  0.45     # same as chic2/chic1 and chib2/chib1
    
    # the following numbers are from an old 3P gun simulation
    # that needs to be re-done
    
    sigma1    =  0.003#0.0031 
    sigma2    =  0.003#0.0035
    
    alpha1    =  0.95
    alpha2    =  1.12

    n         =  2.5  


    mass1_v   = RooRealVar('mchi1','m_{#chi1}',mass_chib)
    deltaM_v  = RooRealVar('deltaM','#Delta_{m}',deltaM,0.005,0.015)
    mass2_v   = RooFormulaVar('mchi2','@0+@1',RooArgList(mass1_v,deltaM_v))
    sigma1_v  = RooRealVar('sigma1','#sigma_1',sigma1)
    sigma2_v  = RooRealVar('sigma2','#sigma_2',sigma2)

    alpha1_v  = RooRealVar('alpha1','#alpha_1',alpha1)
    alpha2_v  = RooRealVar('alpha2','#alpha_2',alpha2)

    n_v       = RooRealVar('n','n',n)

    ratio21_v = RooRealVar('ratio21','r_{21}',ratio21)

    
    x = RooRealVar("invm3S","#chi_{b} Data",10.4,10.7)

    # choose here binning of mass plot
    x.setBins(150)


    #signal pdf
    chib1 = RooCBShape('chib1','chib1',x,mass1_v,sigma1_v,alpha1_v,n_v)
    chib2 = RooCBShape('chib2','chib2',x,mass2_v,sigma2_v,alpha2_v,n_v)
 
    
    # define background
    q01S_Start = 10.4
    alpha =    RooRealVar("#alpha","#alpha",1.5,0.2,3.5)
    beta =     RooRealVar("#beta","#beta",-2.5,-7.,0.)
    #q0   =      RooRealVar("q0","q0",q01S_Start,q01S_Start-0.05,q01S_Start+0.05)
    q0   =      RooRealVar("q0","q0",q01S_Start)
    delta =     RooFormulaVar("delta","TMath::Abs(@0-@1)",RooArgList(x,q0))
    b1 =        RooFormulaVar("b1","@0*(@1-@2)",RooArgList(beta,x,q0))
    signum1 =   RooFormulaVar( "signum1","( TMath::Sign( -1.,@0-@1 )+1 )/2.", RooArgList(x,q0) )

    background = RooGenericPdf("background","Background", "signum1*pow(delta,#alpha)*exp(b1)", RooArgList(signum1,delta,alpha,b1) )


 
 
    n_evts_1 = RooRealVar('N_{3P_{1}}','N_{3P_{1}}',50,30,1000)
    n_evts_2 = RooFormulaVar('N_{3P_{2}}','@0*@1',RooArgList(n_evts_1,ratio21_v))
    n_bck    = RooRealVar('nbkg','n_{bkg}',500,0,100000)


    #build final pdf
    modelPdf = RooAddPdf('ModelPdf', 'ModelPdf', RooArgList(chib1,chib2,background),RooArgList(n_evts_1,n_evts_2,n_bck))
    
    # fit
    low_cut = x.setRange("low_cut",10.4,10.7)
    result = modelPdf.fitTo(roodataset, RooFit.Save(), RooFit.Range("low_cut") )
   
    frame = x.frame(RooFit.Title("m(#chi_{b}(3P))"))
    roodataset.plotOn(frame, RooFit.MarkerSize(0.7))
    modelPdf.plotOn(frame, RooFit.LineWidth(1))


    modelPdf.plotOn(frame, RooFit.LineWidth(2) )

    frame.GetXaxis().SetTitle('m_{#gamma #mu^{+} #mu^{-}} - m_{#mu^{+} #mu^{-}} + m^{PDG}_{#Upsilon(3S)}  [GeV/c^{2}]' )
    #frame.GetYaxis().SetTitle( "Events/15.0 MeV " )
    frame.GetXaxis().SetTitleSize(0.04)
    frame.GetYaxis().SetTitleSize(0.04)
    frame.GetXaxis().SetTitleOffset(1.1)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetLabelSize(0.04)

    frame.SetLineWidth(1)
    frame.SetName("fit_resonance")

    chi2 = frame.chiSquare()
    chi2 = round(chi2,2)
    leg=TLegend(0.50,0.7,0.60,0.8)
    leg.AddEntry(0,'#chi^{2} ='+str(chi2),'')
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.06)

    gROOT.SetStyle("Plain")

    frame.SaveAs(str(hname) + '.root')

#   param_set = RooArgSet(n_evts_Roo4, m_chib[1][3],alpha, beta, q0)

    canvas = TCanvas('fit', "", 1400, 700 )
    canvas.Divide(1)
    canvas.cd(1)
    gPad.SetRightMargin(0.3)
    gPad.SetFillColor(10)
#   modelPdf.paramOn(frame, RooFit.Layout(0.725,0.9875,0.9), RooFit.Parameters(param_set))
    modelPdf.paramOn(frame, RooFit.Layout(0.725,0.9875,0.9))
    frame.Draw()
    leg.Draw("same")
    canvas.SaveAs( str(hname) + '.png' )

if __name__ == '__main__':
    main()
