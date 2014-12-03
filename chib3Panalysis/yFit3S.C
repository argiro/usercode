#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

#include "TStyle.h"
#include "RooDataSet.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "TCanvas.h"
#include "RooAbsPdf.h"
#include "RooAddPdf.h"
#include "RooCBShape.h"
#include "RooPolynomial.h"
#include "RooFitResult.h"
#include "TFile.h"
#include "TTree.h"

using namespace std;
using namespace RooFit;

void DoFit(string dataset, int task_level=0, int ncpu=4);

int main( int argc, char **argv ) {
  if ( argc < 2 ) {
    cout << "Usage: " << argv[0] << " <dataset-file> <task_level> ...\n";
    cout << "supply all parameters... ;-)\n";
    return (-1);
  }
  if ( argc > 2) {
    if ( argc > 3 ) DoFit( argv[1], atoi(argv[2]), atoi(argv[3]) ); 
    else DoFit( argv[1], atoi(argv[2]) );
  } else DoFit( argv[1] ); 
  return 0;
}

void DoFit(string dataset, int task_level, int ncpu) {

/*
task_level = 0  for testing data input
             1  for plotting data input
             2  for fitting mass
             3  for fitting and plotting mass
*/

  cout << "Will use dataset " << dataset.c_str() << endl;
  cout << "Will perform " << task_level << " task with " << ncpu << " threads " << endl;

  gStyle->SetCanvasColor(0);
  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameBorderSize(0);
  gStyle->SetDrawBorder(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetOptTitle(0);

// Definition of input data variables
  RooRealVar mass("ups_mass",     "M(#mu^{+} #mu^{-})",    7.,  11,"GeV/c^{2}");
  RooRealVar    y("ups_rapidity", "y(#mu^{+} #mu^{-})",    -3,   3);
  RooRealVar   pt("ups_pt",       "p_{T}(#mu^{+} #mu^{-})", 0, 100,"GeV/c");

  string tree_name = "rootuple/upsTree";  

  cout << "Importing " << tree_name << " tree from " << dataset << " file" <<endl; 
  TFile *f = new TFile(dataset.c_str(),"READ");
  TTree *tree = (TTree*)f->Get(tree_name.c_str());
  Long64_t nentries = tree->GetEntries();
  cout << "Tree read with " << nentries << " entries" << endl;
 
  string cuts  = "abs(ups_rapidity) < 1.25 && ups_pt>9.5";

  cout << "Getting dataset " << endl;
  RooDataSet data("yds","Total Y dataset",RooArgSet(mass,y,pt),Import(*tree));
  RooDataSet* reduced_ds = (RooDataSet*) data.reduce(cuts.c_str());
  reduced_ds->SetNameTitle("reduced_ds","Y dataset");
  f->Close();

  data.Print();
  reduced_ds->Print();
  if ( task_level == 0 ) return;

  mass.setRange(8.5,11.);
  if ( task_level == 1 ) {
    TCanvas *cData = new TCanvas("cData","Input Data");
    RooPlot *frameM = mass.frame(250);
    data.plotOn(frameM);
    reduced_ds->plotOn(frameM);
    frameM->Draw();
    cData->SaveAs("plot-mass-input.png");
    cData->Close();
    return;
  }

  string hname = "Y3S";

  cout << "Performing fit" << endl;

//.. model signal
//.. one CB for each Y(nS) or sum of two CB for each Y(nS)

//.. CB parameters
  RooRealVar mass1S("mass1S","mass1S",  9.4603, 9.400,  9.500);
  RooRealVar mass2S("mass2S","mass2S", 10.022, 10.000, 10.040);
  RooRealVar mass3S("mass3S","mass3S", 10.3552,10.300, 10.370);

  RooRealVar sigma1S_1("sigma1S_1","sigma1S_1",0.080,0.010,0.100);
  RooRealVar sigma1S_2("sigma1S_2","sigma1S_2",0.085,0.010,0.100);
  RooRealVar sigma2S_1("sigma2S_1","sigma2S_1",0.085,0.020,0.100);
  RooRealVar sigma2S_2("sigma2S_2","sigma2S_2",0.090,0.020,0.100);
  RooRealVar sigma3S_1("sigma3S_1","sigma3S_1",0.090,0.020,0.100);
  RooRealVar sigma3S_2("sigma3S_2","sigma3S_2",0.095,0.020,0.100);

  RooRealVar alpha("alpha","alpha",0.5,0,5);
  RooRealVar n("n","n",0.5,0,5); // fix n

//.. signal model
  RooCBShape cb1S_1("cb1S_1","y1S_1",mass, mass1S,sigma1S_1, alpha,n);
  RooCBShape cb1S_2("cb1S_2","y1S_2",mass, mass1S,sigma1S_2, alpha,n);
  RooCBShape cb2S_1("cb2S_1","y2S_1",mass, mass2S,sigma2S_1, alpha,n);
  RooCBShape cb2S_2("cb2S_2","y2S_2",mass, mass2S,sigma2S_2, alpha,n);
  RooCBShape cb3S_1("cb3S_1","y3S_1",mass, mass3S,sigma3S_1, alpha,n);
  RooCBShape cb3S_2("cb3S_2","y3S_2",mass, mass3S,sigma3S_2, alpha,n);

  RooRealVar cb1frac1S("cb1frac1S","cc 1",0.1,0.,1.);
  RooRealVar cb1frac2S("cb1frac2S","cc 2",0.1,0.,1.);
  RooRealVar cb1frac3S("cb1frac3S","cc 3",0.1,0.,1.);

//.. sum of two CB
  RooAddPdf sig1S("sig1S","Signal1S",RooArgList(cb1S_1,cb1S_2),RooArgList(cb1frac1S));
  RooAddPdf sig2S("sig2S","Signal2S",RooArgList(cb2S_1,cb2S_2),RooArgList(cb1frac2S));
  RooAddPdf sig3S("sig3S","Signal3S",RooArgList(cb3S_1,cb3S_2),RooArgList(cb1frac3S));

//.. background model
  RooRealVar c1("c1","c1",200,0,3000000);
  RooRealVar c2("c2","c2",-1,-50,50);
  RooPolynomial background("background","bkg", mass, RooArgList(c1,c2));

//.. complete model

  RooRealVar n1S("n1S",  "n1s",100000,0,10000000);
  RooRealVar n2S("n2S",  "n2s",100000,0,10000000);
  RooRealVar n3S("n3S",  "n3s",100000,0,10000000);
  RooRealVar nbck("nbck","nbk",100000,0,10000000);

//.. sum of two CB for each Y(nS)
  RooAddPdf  modelPdf("modelPdf","model",RooArgList(sig1S,sig2S,sig3S,background),RooArgList(n1S,n2S,n3S,nbck));

//.. or one CB for each Y(nS)
  //RooAddPdf modelPdf("modelPdf","model",RooArgList(cb1S_1,cb2S_1,cb3S_1,background),RooArgList(n1S,n2S,n3S,nbck));

  RooFitResult *result = modelPdf.fitTo(*reduced_ds,Save(),NumCPU(ncpu),Timer());
  result->Print("v");

  if ( task_level == 2) return;

  RooPlot *frameM = mass.frame(250);
  reduced_ds->plotOn(frameM,MarkerSize(0.7));
  modelPdf.plotOn(frameM,LineWidth(2),LineColor(kBlack));
  TCanvas *cData = new TCanvas("cData","Fitted Data",1400,700);
  cData->Divide(1);
  cData->cd(1);
  gPad->SetRightMargin(0.3);
  gPad->SetFillColor(10);
  modelPdf.paramOn(frameM,Layout(0.725,0.9875,0.9));
  frameM->Draw();
  string hnamefile = hname + ".png";
  cData->SaveAs(hnamefile.c_str());
  cData->Close();
  return;
}
