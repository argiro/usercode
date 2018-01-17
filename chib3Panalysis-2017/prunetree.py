#
# manipulate branch names to be able to perform simultaneosu fit to 1,2,3S
#

from ROOT import TTree,TFile
import ROOT



# 2S
oldfile = TFile('data/filtered-all-chib-2S.root')

# 3S
oldfile = TFile('data/filtered-all-chib-3S.root')



oldtree = oldfile.Get('chibTree')
oldtree.SetBranchStatus('invm1S',0)


#for 2S
#newfile = TFile('2012_AllData_v2_pruned.root','recreate')

# for 3S
newfile = TFile('2012_AllData_v2_pruned3S.root','recreate')

#newfile.mkdir('rootuple')
#newfile.cd('rootuple')
newtree = oldtree.CloneTree()

# for 2S 
#newtree.GetBranch("invm2S").SetName("invm1S")
#newtree.GetBranch("invm1S").SetTitle("invm1S")

# for 3S
newtree.GetBranch("invm3S").SetName("invm1S")
newtree.GetBranch("invm1S").SetTitle("invm1S")

newtree.Write('',ROOT.TObject.kOverwrite)
