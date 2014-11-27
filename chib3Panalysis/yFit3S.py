#
# Fit Y -> mumu spectrum
#
# Stefano Argiro', University of Turin and INFN
#
#
#

from ROOT import RooDataSet, RooRealVar, RooArgSet, RooFormulaVar, RooGenericPdf, RooCmdArg, RooStats
from ROOT import RooCBShape, RooAddPdf, RooArgList, RooPlot, RooDataHist, RooFitResult, RooAbsPdf,RooGaussian, RooPolynomial
from ROOT import RooFit, gROOT, TStyle, gStyle, gPad
from ROOT import TFile, TCanvas, TH1F, TGraphErrors, TPad, TLegend, TPaveText, TMultiGraph, TGraphErrors, TMath
from ROOT import TH1F, TTree, RooHistPdf
import ROOT
import sys

def main() :

    # setting for reduced DS to be used on the output of makeSubset.C

    inputfile_name = "small.root"
    tree_name = "upsTree"     

    # settings for full dataset (long processing time for unbinned lh)    
    #inputfile_name = "/data1/chibdata/collision/v2/2012_AllData_v2.root"
    #tree_name = "rootuple/upsTree"

    
    print "Opening file"
    inputfile = TFile.Open(inputfile_name,"READ")
    print "Importing tree"
    tree = TTree()
    inputfile.GetObject(tree_name, tree)

    mass = RooRealVar("ups_mass", "ups_mass", 7, 11)
    y = RooRealVar("ups_rapidity", "ups_rapidity", -3, 3)
    pt = RooRealVar("ups_pt", "ups_pt", 0,100)
    


    print "Assigning dataset"
    dataArgSet = RooArgSet(mass,y,pt)

    dataSet= RooDataSet("yds","Y data set",tree, dataArgSet)

    cuts=  "abs(ups_rapidity) < 1.25"+\
           "&& ups_pt>9.5"\

    reduced_ds = dataSet.reduce(RooFit.Cut(cuts))

    print "Performing likelihood analysis"
    dofit(reduced_ds,"Y3S")


def dofit(roodataset,hname):

    x = RooRealVar("ups_mass","m_{#mu #mu}",8.5,11.0)

    # choose here binning of mass plot
    x.setBins(250)


    # model signal
    # one CB for each Y(nS) or sum of two CB for each Y(nS)
    
    # CB parameters
    mass1S = RooRealVar('mass1S','mass1S', 9.4603, 9.400, 9.500)
    mass2S = RooRealVar('mass2S','mass2S', 10.022, 10.000, 10.040)
    mass3S = RooRealVar('mass3S','mass3S', 10.3552,10.300, 10.370)

    sigma1S_1 = RooRealVar('sigma1S_1','sigma1S_1',0.080,0.010,0.100)
    sigma1S_2 = RooRealVar('sigma1S_2','sigma1S_2',0.085,0.010,0.100)
    sigma2S_1 = RooRealVar('sigma2S_1','sigma2S_1',0.085,0.020,0.100)
    sigma2S_2 = RooRealVar('sigma2S_2','sigma2S_2',0.090,0.020,0.100)
    sigma3S_1 = RooRealVar('sigma3S_1','sigma3S_1',0.090,0.020,0.100)
    sigma3S_2 = RooRealVar('sigma3S_2','sigma3S_2',0.095,0.020,0.100)

    alpha = RooRealVar('alpha','alpha',0.5,0,5)
    n     = RooRealVar('n','n',0.5,0,5) # fix n
    
    #signal model
    cb1S_1 =  RooCBShape ('y1S_1','y1S_1',x, mass1S,sigma1S_1, alpha,n)
    cb1S_2 =  RooCBShape ('y1S_2','y1S_2',x, mass1S,sigma1S_2, alpha,n)
    cb2S_1 =  RooCBShape ('y2S_1','y2S_1',x, mass2S,sigma2S_1, alpha,n)
    cb2S_2 =  RooCBShape ('y2S_2','y2S_2',x, mass2S,sigma2S_2, alpha,n)
    cb3S_1 =  RooCBShape ('y3S_1','y3S_1',x, mass3S,sigma3S_1, alpha,n)
    cb3S_2 =  RooCBShape ('y3S_2','y3S_2',x, mass3S,sigma3S_2, alpha,n)

    cb1frac1S=RooRealVar("cb1frac1S","cc",0.1,0.,1.) 
    cb1frac2S=RooRealVar("cb1frac2S","cc",0.1,0.,1.) 
    cb1frac3S=RooRealVar("cb1frac3S","cc",0.1,0.,1.) 

    # sum of two CB
    sig1S=RooAddPdf("sig1S","Signal1S",RooArgList(cb1S_1,cb1S_2),RooArgList(cb1frac1S))
    sig2S=RooAddPdf("sig2S","Signal2S",RooArgList(cb2S_1,cb2S_2),RooArgList(cb1frac2S))
    sig3S=RooAddPdf("sig3S","Signal3S",RooArgList(cb3S_1,cb3S_2),RooArgList(cb1frac3S)) 

    
    
    #background model
    c1 =RooRealVar('c1','c1',200,0,3000000)
    c2 =RooRealVar('c2','c2',-1,-50,50)
    background = RooPolynomial('bkg','bkg', x, RooArgList(c1,c2))


    # complete model

    n1S =RooRealVar('n1s','',100000,0,10000000)
    n2S =RooRealVar('n2s','',100000,0,10000000)
    n3S =RooRealVar('n3s','',100000,0,10000000)
    nbck=RooRealVar('nbck','',100000,0,10000000)

    # sum of two CB for each Y(nS)
    modelPdf = RooAddPdf('model','model',RooArgList(sig1S,sig2S,sig3S,background),RooArgList(n1S,n2S,n3S,nbck))

    # or one CB for each Y(nS)
    #modelPdf = RooAddPdf('model','model',RooArgList(cb1S_1,cb2S_1,cb3S_1,background),RooArgList(n1S,n2S,n3S,nbck))

    rcut = x.setRange('rcut',8.5,11.0)
    result = modelPdf.fitTo(roodataset,RooFit.Save(), RooFit.Range('rcut'))


    frame = x.frame(RooFit.Title('mass'))
    roodataset.plotOn(frame, RooFit.MarkerSize(0.7))
    
    modelPdf.plotOn(frame, RooFit.LineWidth(2) )


    #plotting
    canvas = TCanvas('fit', "", 1400, 700 )
    canvas.Divide(1)
    canvas.cd(1)
    gPad.SetRightMargin(0.3)
    gPad.SetFillColor(10)
    modelPdf.paramOn(frame, RooFit.Layout(0.725,0.9875,0.9))
    frame.Draw()
    canvas.SaveAs( str(hname) + '.png' )



if __name__ == '__main__':
    main()
