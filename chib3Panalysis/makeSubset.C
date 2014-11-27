void makeSubset() {

   unsigned int ntocopy = 100000; 

   //Get old file, old tree and set top branch address
   TFile *oldfile = new TFile("/data1/chibdata/collision/v2/2012_AllData_v2.root");
   TTree *oldtree = (TTree*)oldfile->Get("rootuple/upsTree");
   Long64_t nentries = oldtree->GetEntries();

   double ups_mass,ups_rapidity,ups_pt; 
   oldtree->SetBranchAddress("ups_mass",&ups_mass);
   oldtree->SetBranchAddress("ups_rapidity",&ups_rapidity);
   oldtree->SetBranchAddress("ups_pt",&ups_pt);

   //Create a new file + a clone of old tree in new file
   TFile *newfile = new TFile("small.root","recreate");
   TTree *newtree = oldtree->CloneTree(0);

   for (Long64_t i=0;i<ntocopy; i++) {
      oldtree->GetEntry(i);
      newtree->Fill();
      ups_mass=ups_rapidity=ups_pt=0;
   }

   newtree->AutoSave();
   delete oldfile;
   delete newfile;
}
