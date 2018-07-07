#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  craneenContentModule import *
from  exampleModule import *

preselection="nJet >= 6 && Jet_pt[5]>30 && ((Muon_pt[0]>30) || (Electron_pt[0]>30))"
files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]
p=PostProcessor(".",files,preselection,"keep_and_drop_verytight.txt",[craneenContentModule()],provenance=True)
#p=PostProcessor(".",files,preselection,"keep_and_drop.txt",[exampleModule()],provenance=True)
p.run()
