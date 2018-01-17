from ROOT import RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooGenericPdf, RooCmdArg, RooStats
from ROOT import RooCBShape, RooAddPdf, RooArgList, RooPlot, RooDataHist, RooFitResult, RooAbsPdf, RooVoigtian
from ROOT import RooFit, gROOT, TStyle, gStyle, gPad
from ROOT import TFile, TCanvas, TH1F, TGraphErrors, TPad, TLegend, TPaveText, TMultiGraph, TGraphErrors, TMath
from ROOT import TH1F, TTree
from ROOT import gSystem
gSystem.Load('My_double_CB/My_double_CB_cxx')
from ROOT import My_double_CB


def fitChicSpectrum(dataset,binname):
    """ Fit chic spectrum"""


    x = RooRealVar('Qvalue','Q',9.7,10.1)
    x.setBins(80)




    mean_1 = RooRealVar("mean_1","mean ChiB1",9.892,9,10,"GeV")
    sigma_1 = RooRealVar("sigma_1","sigma ChiB1",0.0058,'GeV')
    a1_1 = RooRealVar('#alpha1_1', '#alpha1_1', 0.748)
    n1_1 = RooRealVar('n1_1', 'n1_1',2.8 )
    a2_1 = RooRealVar('#alpha2_1', '#alpha2_1',1.739)
    n2_1 = RooRealVar('n2_1', 'n2_1', 3.0)


    deltam = RooRealVar('deltam','deltam',0.01943)
    
    mean_2 = RooFormulaVar("mean_2","@0+@1", RooArgList(mean_1,deltam))
    sigma_2 = RooRealVar("sigma_2","sigma ChiB2",0.0059,'GeV')
    a1_2 = RooRealVar('#alpha1_2', '#alpha1_2', 0.738)
    n1_2 = RooRealVar('n1_2', 'n1_2', 2.8)
    a2_2 = RooRealVar('#alpha2_2', '#alpha2_2', 1.699)
    n2_2 = RooRealVar('n2_2', 'n2_2', 3.0)

    
    parameters=RooArgSet()
    
    parameters.add(RooArgSet(sigma_1, sigma_2))
    parameters = RooArgSet(a1_1, a2_1, n1_1, n2_1)
    parameters.add(RooArgSet( a1_2, a2_2, n1_2, n2_2))
 
    chib1_pdf = My_double_CB('chib1', 'chib1', x, mean_1, sigma_1, a1_1, n1_1, a2_1, n2_1)
    chib2_pdf = My_double_CB('chib2', 'chib2', x, mean_2, sigma_2, a1_2, n1_2, a2_2, n2_2)

    
    #background
    q01S_Start = 9.5
    alpha   =   RooRealVar("#alpha","#alpha",1.5,-1,3.5)#0.2 anziche' 1
    beta    =   RooRealVar("#beta","#beta",-2.5,-7.,0.)
    q0      =   RooRealVar("q0","q0",q01S_Start)#,9.5,9.7)
    delta   =   RooFormulaVar("delta","TMath::Abs(@0-@1)",RooArgList(x,q0))
    b1      =   RooFormulaVar("b1","@0*(@1-@2)",RooArgList(beta,x,q0))
    signum1 =   RooFormulaVar( "signum1","( TMath::Sign( -1.,@0-@1 )+1 )/2.", RooArgList(x,q0) )
    
    
    background = RooGenericPdf("background","Background", "signum1*pow(delta,#alpha)*exp(b1)", RooArgList(signum1,delta,alpha,b1) )

    parameters.add(RooArgSet(alpha, beta, q0))

    #together
    chibs = RooArgList(chib1_pdf,chib2_pdf,background)    

    

    n_chib = RooRealVar("n_chib","n_chib",2075, 0, 100000)
    ratio_21 = RooRealVar("ratio_21","ratio_21",0.5,0,1)
    n_chib1 = RooFormulaVar("n_chib1","@0/(1+@1)",RooArgList(n_chib, ratio_21))
    n_chib2 = RooFormulaVar("n_chib2","@0/(1+1/@1)",RooArgList(n_chib, ratio_21))
    n_background = RooRealVar('n_background','n_background',4550, 0, 50000)
    ratio_list = RooArgList(n_chib1, n_chib2, n_background)


    modelPdf = RooAddPdf('ModelPdf', 'ModelPdf', chibs, ratio_list)


    frame = x.frame(RooFit.Title('m'))
    range = x.setRange('range',9.7,10.1)
    result = modelPdf.fitTo(dataset,RooFit.Save(),RooFit.Range('range'))
    dataset.plotOn(frame,RooFit.MarkerSize(0.7))

    modelPdf.plotOn(frame, RooFit.LineWidth(2) )

    
    #plotting
    canvas = TCanvas('fit', "", 1400, 700 )
    canvas.Divide(1)
    canvas.cd(1)
    gPad.SetRightMargin(0.3)
    gPad.SetFillColor(10)
    modelPdf.paramOn(frame, RooFit.Layout(0.725,0.9875,0.9))
    frame.Draw()
    canvas.SaveAs( 'out-'+binname + '.png' )

    
if __name__ == '__main__':

    #infile = TFile('/data1/chibdata/collision/v2/RooDataSets/chicDataSet.root')
    #infile = TFile('data-ds-corr.root')

    #infile = TFile('data-ds-corr-chiib.root')

    infile = TFile('chibds-s-kinfit-corr.root')
    
    #infile = TFile('chibDataSet.root')
    #infile = TFile('chicDataSet-100k.root')
    #infile = TFile('m2.root')

    cuts = '   abs(y_mumu)<1.25'+\
           '&& pt_mumu>11'+\
           '&& rho_conv >1.5'+\
           '&& dz<0.1'+\
           '&& psi1S_nsigma<3.0'+\
           '&& pt_gamma > 0.5'+\
           '&& eta_gamma < 1.0'
    
    ds = infile.Get('chicds')

    #pt_gamma_min =[0.0,0.8 ,1.25,2.0]
    #pt_gamma_max =[0.8,1.25,2.0 ,5.0]
    
    pt_gamma_min = [1.0, 1.25, 1.55, 1.95,  2.55]
    pt_gamma_max = [1.25, 1.55, 1.95, 2.55, 5.0]
    
    #for ptmin,ptmax in zip(pt_gamma_min,pt_gamma_max):
    #    binname = str(ptmin) + '-'+str(ptmax)
    #    ptcuts = '&& pt_gamma >' + str(ptmin) + '&& pt_gamma<'+str(ptmax)
    #    fitChicSpectrum(ds.reduce(cuts+ptcuts),binname)

    fitChicSpectrum(ds.reduce(cuts),'chib-qdscb-kinfit-corr-all')

        
