from ROOT import RooFit, gROOT, TStyle, gStyle, gPad
from ROOT import TFile, TCanvas, TH1F, TGraphErrors, TPad, TLegend, TPaveText, TMultiGraph, TMath
from ROOT import TTree, TLorentzVector
from ROOT import RooRealVar, RooArgSet, RooDataSet
from array import array
import getopt,sys

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


#chic_tree_file  = '/data1/chibdata/chicfullmc/tuple-rec-chic-mc.root'
chic_tree_file = 'data/filtered-all-chic-1S.root'
#chic_tree_file = '/data2/data/degano/chic_MonteCarlo_March2014/CMSSW_5_3_3/src/chic_rootuple_MC_15M_sel.root'
chic_tree_name = 'chictree'

chib_tree_file = '/data1/chibdata/collision/v2/2012_AllData_v2.root'
chib_tree_name = 'rootuple/chibTree'


def makeRooDataSet(type,infile_name,outfile_name,tree_name,nevents):
    """ Make RooDataSets from TTrees"""




    inputfile = TFile.Open(infile_name,"READ")
    print "Importing tree"
    tree = TTree()
    inputfile.GetObject(tree_name, tree)  #get the tree from the data file

   

    #define variables for the RooDataSet
    m_mumu        = RooRealVar("m_mumu",   "m_mumu",   0.0, 4.0)
    y_mumu        = RooRealVar("y_mumu",   "y_mumu",   0.0, 2.0 )
    pt_mumu       = RooRealVar("pt_mumu",  "pt_mumu",  0.0, 260.0)
    eta_gamma     = RooRealVar("eta_gamma","eta_gamma",-3.5, 3.5)
    pt_gamma      = RooRealVar("pt_gamma", "pt_gamma", 0.0, 100.0)
    m_gamma       = RooRealVar("m_gamma",  "m_gamma",  -0.1,0.1)
  
    m_chi_rf1S    = RooRealVar("m_chi_rf1S", "m_chi_rf1S", 0.0, 7.0)
    m_chi_rf2S    = RooRealVar("m_chi_rf2S", "m_chi_rf2S", -1.0, 1.0)
    #Qvalue        = RooRealVar("Qvalue","Q", -15., 15.)
    s             = RooRealVar("s","s", -10., 10.)
    
    ctpv          = RooRealVar("ctpv","ctpv", -1.0, 3.5)
    ctpv_error    = RooRealVar("ctpv_err","ctpv_err", -1.0, 1.0)
    pi0_abs_mass  = RooRealVar("pi0_abs_mass","pi0_abs_mass", 0.0, 2.2)
    psi1S_nsigma  = RooRealVar("psi1S_nsigma","psi1S_nsigma",0.0,1.0)
    psi2S_nsigma  = RooRealVar("psi2S_nsigma","psi2S_nsigma",0.0,1.0)
    psi3S_nsigma  = RooRealVar("psi3S_nsigma","psi3S_nsigma",0.0,1.0)
    rho_conv      = RooRealVar("rho_conv", "rho_conv", 0.0, 70.0)
    dz            = RooRealVar("dz","dz", -1.0, 1.0)
    probFit1S     = RooRealVar("probFit1S","probFit1S",0,1)
    probFit2S     = RooRealVar("probFit2S","probFit2S",0,1)

    dataArgSet = RooArgSet(m_mumu,
                           y_mumu,
                           pt_mumu,
                           eta_gamma,
                           pt_gamma,
                           m_gamma, 
                           m_chi_rf1S)
    
    dataArgSet.add( m_chi_rf2S )
    dataArgSet.add( s )
    dataArgSet.add( ctpv )
    dataArgSet.add( ctpv_error )
    dataArgSet.add( pi0_abs_mass )
    dataArgSet.add( psi1S_nsigma )
    dataArgSet.add( psi2S_nsigma )
    dataArgSet.add( rho_conv )
    dataArgSet.add( dz )
    dataArgSet.add( probFit1S )
    dataArgSet.add( probFit2S )


    print "Creating DataSet"
    dataSet = RooDataSet("chicds","Chic RooDataSet", dataArgSet)

    entries = tree.GetEntries()
    print entries

    if nevents is not 0:
        entries = nevents

    for ientry in range(0,entries):
        tree.GetEntry(ientry)

        # unfort ntuples are slightly different for chic and chib
        
        if type == 'chic':
            
            m_mumu.setVal(tree.dimuon_mass)
            y_mumu.setVal(tree.dimuon_rapidity)        
            pt_mumu.setVal(tree.dimuon_pt)
            eta_gamma.setVal(tree.photon_eta)
            pt_gamma.setVal(tree.photon_pt)
            #m_gamma.setVal(tree.photon_p4.M())
            m_chi_rf1S.setVal(tree.rf1S_chic_mass)
            #m_chi_rf1S.setVal(tree.rf2S_chi_p4.M())
            #Qvalue.setVal((tree.chi_p4).M() - tree.dimuon_p4.M())
            #Qvalue.setVal((tree.chi_p4).M()**2 - tree.dimuon_p4.M()**2)
            #Qvalue.setVal((tree.rf1S_chic_mass**2 -tree.dimuon_mass**2)
            #              / (3.5107**2 - 3.0969**2 ) -1)

            
#           this should be the correct one if the refitted variable was available
#           s.setVal((tree.rf1S_chic_mass**2 - tree.rf1S_dimuon_p4.M()**2)/ (3.5107**2 - 3.0969**2 ) -1)
             
            s.setVal((tree.rf1S_chic_mass**2 - 3.0969**2)/ (3.5107**2 - 3.0969**2 ) -1)


            
            psi1S_nsigma.setVal(tree.psi1S_nsigma)
            psi2S_nsigma.setVal(0)  
            psi3S_nsigma.setVal(0)
            
        elif type == 'chib':

            m_mumu.setVal(tree.dimuon_mass)
            y_mumu.setVal(tree.dimuon_rapidity)        
            pt_mumu.setVal(tree.dimuon_pt)
            eta_gamma.setVal(tree.photon_eta)
            pt_gamma.setVal(tree.photon_pt)
            m_chi_rf1S.setVal(tree.rf1S_chib_mass)
            m_chi_rf2S.setVal(tree.rf2S_chib_mass)        
            Qvalue.setVal(tree.chib_mass - tree.dimuon_mass)
            psi1S_nsigma.setVal(tree.Y1S_nsigma)
            psi2S_nsigma.setVal(tree.Y2S_nsigma) 
            psi3S_nsigma.setVal(tree.Y3S_nsigma)
        
        ctpv.setVal(tree.ct_pv)
        ctpv_error.setVal(tree.ct_pv_error)
        #pi0_abs_mass.setVal(tree.pi0_abs_mass)

        rho_conv.setVal(tree.Conv)
        dz.setVal(tree.Dz)
        probFit1S.setVal(tree.probfit1S)
        #probFit2S.setVal(tree.probFit2S)
        
        #if (tree.chic_pdgId == 20443):dataSet.add(dataArgSet)
        dataSet.add(dataArgSet)
        

    outfile = TFile(outfile_name,'recreate')    
    dataSet.Write()
      

def usage():
    print "makeRooDataset.py -t [chic/chib] -o [outfile] [-h]"



if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:o:hn:", ["type=","out=","help","nevents="])
    except getopt.GetoptError as err:
        usage()        
        sys.exit(2)
        
        
    type = None
    outfile = 'out.root'
    nevents =0
    
    for o, a in opts:
        if o in ("-t","--type"):
            if a =="chic":
                infile    = chic_tree_file
                tree_name = chic_tree_name
                type = a
            elif a == "chib":    
                infile =    chib_tree_file 
                tree_name=  chib_tree_name
                type = a
            else :
                print 'Unrecognized type, only chib and chic are known'
                sys.exit(2)
                
        elif o in ("-h", "--help"):
            usage()
            sys.exit()

        elif o in ("-o","--out"):
            outfile = a

        elif o in ("-n","--nevents"):
            nevents = int(a)
            
    makeRooDataSet(type,infile,outfile,tree_name,nevents)
