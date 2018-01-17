from ROOT import RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooGenericPdf, RooCmdArg, RooStats
from ROOT import RooCBShape, RooAddPdf, RooArgList, RooPlot, RooDataHist, RooFitResult, RooAbsPdf, RooVoigtian
from ROOT import RooFit, gROOT, TStyle, gStyle, gPad
from ROOT import TFile, TCanvas, TH1F, TGraphErrors, TPad, TLegend, TPaveText, TMultiGraph, TGraphErrors, TMath
from ROOT import TH1F, TTree


def fitChicSpectrum(dataset,binname):
    """ Fit chic spectrum"""


    x = RooRealVar('s','s',-2,2)
     
    x.setBins(200)
    
    #signal model

    
    q_chi1       = RooRealVar('qchi1','q_{#chi 1}',0.414,0.2,0.6) 
    q_chi2       = RooRealVar('qchi2','q_{#chi 2}',0.430,0.2,0.6)

    delta_chi10  = RooRealVar('delta_chi10','delta_chi10',0.09591)
    q_chi0       = RooFormulaVar('q_chi0','@0 - @1',
                                 RooArgList(q_chi1,delta_chi10))


    alphacb_chi1 = RooRealVar( 'alphacb_chi1','#alpha^{CB}_{#chi 1}',0.6,0,2)
    alphacb_chi2 = RooRealVar( 'alphacb_chi2','#alpha^{CB}_{#chi 2}',0.4,0,2)
    sigmacb_chi1 = RooRealVar( 'sigmacb_chi1','#sigma^{CB}_{#chi 1}',0.005,0,1)
    sigmacb_chi2 = RooRealVar( 'sigmacb_chi2','#sigma^{CB}_{#chi 2}',0.005,0,1)
    n_cb         = RooRealVar( 'ncb','n^{CB}',3.0,0.,5.) 


    gamma_chi0   = RooRealVar('gamma_chi0','gamma_chi0',0.0104)
    sigmacb_chi0 = RooRealVar( 'sigmacb_chi0','#sigma^{CB}_{#chi 0}',0.005)

    chi0_sig = RooVoigtian('chi0sig','chi0sig,',x,q_chi0,sigmacb_chi0,gamma_chi0)
    chi1_sig = RooCBShape ('chi1sig','chi1sig',x,q_chi1,
                           sigmacb_chi1,alphacb_chi1,n_cb)
    chi2_sig = RooCBShape ('chi2sig','chi2sig',x,q_chi2,
                           sigmacb_chi2,alphacb_chi2,n_cb)

    
    fchi0 = RooRealVar   ('fchi0','f_{#chi 0}',0.01,0,1)
    fchi1 = RooRealVar   ('fchi1','f_{#chi 1}',0.5,0,1)
    fchi2 = RooFormulaVar('fchi2','1-@0-@1',RooArgList(fchi0,fchi1))
    fbck  = RooRealVar   ('fbck','f_{bck}',0.2,0,1)

    sigmodel = RooAddPdf('sigm','sigm',RooArgList(chi0_sig,chi1_sig,chi2_sig),
                                       RooArgList(fchi0,fchi1,fchi2))
    

    #background model

    q0Start = 0.0
    a_bck =    RooRealVar('a_bck','a_{bck}',0.5,-5,5)
    b_bck =    RooRealVar('b_bck','b_{bck}',-2.5,-7.,0.)
    q0    =    RooRealVar('q0','q0',q0Start)
    delta =    RooFormulaVar('delta','TMath::Abs(@0-@1)',RooArgList(x,q0))
    bfun  =    RooFormulaVar('bfun','@0*(@1-@2)',RooArgList(b_bck,x,q0))
    signum=    RooFormulaVar( 'signum','( TMath::Sign( -1.,@0-@1 )+1 )/2.',
                              RooArgList(x,q0))

    background = RooGenericPdf('background','Background',
                               'signum*pow(delta,a_bck)*exp(bfun)',
                               RooArgList(signum,delta,a_bck,bfun) )


    
    modelPdf = RooAddPdf('chicmodel',
                         'chicmodel',
                         RooArgList(sigmodel,background),
                         RooArgList(fbck))

    frame = x.frame(RooFit.Title('Q'))
    range = x.setRange('range',0,2)
#    result = modelPdf.fitTo(dataset,RooFit.Save(),RooFit.Range('range'))
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
    canvas.SaveAs( 'out-'+binname + '.root' )
    
if __name__ == '__main__':

    infile = TFile('ds-chic.root')
     
    cuts = '   abs(y_mumu)<1.25'+\
           '&& pt_mumu>10'+\
           '&& rho_conv >1.5'+\
           '&& dz<0.5'+\
           '&& psi1S_nsigma<3.0'
           
    ds = infile.Get('chicds')

    #pt_gamma_min =[0.0,0.8 ,1.25,2.0]
    #pt_gamma_max =[0.8,1.25,2.0 ,5.0]
    
    pt_gamma_min = [1.0, 1.25, 1.55, 1.95,  2.55]
    pt_gamma_max = [1.25, 1.55, 1.95, 2.55, 5.0]
    
    #for ptmin,ptmax in zip(pt_gamma_min,pt_gamma_max):
    #    binname = str(ptmin) + '-'+str(ptmax)
    #    ptcuts = '&& pt_gamma >' + str(ptmin) + '&& pt_gamma<'+str(ptmax)
    #    fitChicSpectrum(ds.reduce(cuts+ptcuts),binname)

    fitChicSpectrum(ds.reduce(cuts),'s-refit')

        
