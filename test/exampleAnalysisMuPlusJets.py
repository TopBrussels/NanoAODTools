#!/usr/bin/env python

# make sure to also check out event content, for example here: https://cms-nanoaod-integration.web.cern.ch/integration/master/mc94X_doc.html
# important: set a tight enough preselection in the preselection object. This speeds up the code substantially

import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class ExampleAnalysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

	self.h_vpt=ROOT.TH1F('sumpt',   'sumpt',   100, 0, 1000)
        self.addObject(self.h_vpt )

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        eventSum = ROOT.TLorentzVector()

	#select events with at least 2 muons
	if len(muons) ==1 :
	  for lep in muons :     #loop on muons
            eventSum += lep.p4()
          for lep in electrons : #loop on electrons
            eventSum += lep.p4()
          for j in jets :       #loop on jets
            eventSum += j.p4()
          self.h_vpt.Fill(eventSum.Pt()) #fill histogram

        return True


preselection="nJet >= 6 && Muon_pt[0]>30"
files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[ExampleAnalysis()],noOut=True,histFileName="histOut.root",histDirName="plots")
p.run()
