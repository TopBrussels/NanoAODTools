from __future__ import (division, print_function)

import ROOT 
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class HistogramMaker(Module): #This line defines our class ExampleModule, and in parenthesis, we indicate it Inherits from the Module class we imported above.
    def __init__(self):
        self.writeHistFile=True #Necessary for an output file to be created? 
        self.counter = 0 #Define this global variable to count events
        self.EventLimit = 100000 #-1 for no limit, anthing larger chosen here will be the limit of events fully processed

    def beginJob(self,histFile=None,histDirName=None):
        #beginJob is typically where histograms should be initialized
        #So we call the default Module's beginJob, passing it the histFile and histDirName first passed to the PostProcessor
        Module.beginJob(self,histFile,histDirName)

        #Create a 1-D histogram (TH1D) with histogram_name h_jets, and someTitle(title)/nJets(x-axis)/Events(y-axis), 20 bins, Domain 0 to 20
        #The histogram then has to be 'booked' with the service that will write everything to the output file via self.addObject()
        self.h_jets = ROOT.TH1D('h_jets', 'someTitle;nJets;Events',   20, 0, 20)
        self.addObject(self.h_jets)
        #Repeat for other histograms
        self.h_fatjets = ROOT.TH1D('h_fatjets', ';nFatJets;Events', 8, 0, 8)
        self.addObject(self.h_fatjets)
        self.h_subjets = ROOT.TH1D('h_subjets', ';nSubJets;Events', 16, 0, 16)
        self.addObject(self.h_subjets)
        self.h_jet_map = ROOT.TH2F('h_jet_map', ';Jet Eta;Jet Phi', 40, -2.5, 2.5, 20, -3.14, 3.14)
        self.addObject(self.h_jet_map)
        self.h_medCSVV2 = ROOT.TH1D('h_medCSVV2', ';Medium CSVV2 btags; Events', 5, 0, 5)
        self.addObject(self.h_medCSVV2)
        self.h_medDeepB = ROOT.TH1D('h_medDeepB', ';Medium DeepCSV btags; Events', 5, 0, 5)
        self.addObject(self.h_medDeepB)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.counter += 1
        
        #Below we 'halt' execution for events past the first N (20 when written) by returning False now 
        if self.counter > self.EventLimit > -1:
            return False
        
        ###########################################
        ###### Basic Attributes of the Event ######
        ###########################################
        #Use basic python getattr() method to grab this info, no need for Object or Collection here
        run = getattr(event, "run")
        lumi = getattr(event, "luminosityBlock")
        evt = getattr(event, "event")
        #print("\n\nRun: {0:>8d} \tLuminosityBlock: {1:>8d} \tEvent: {2:>8d}".format(run,lumi,evt)) 

        ###########################################
        ###### Event Collections and Objects ######
        ###########################################
        #Collections are for variable-length objects, easily identified by a nVARIABLE object in the NanoAOD file ("nJet")
        #Objects are for 1-deep variables, like HLT triggers, where there are many of them, but there is only one boolean value
        #for each HLT_SomeSpecificTrigger in the event. These are more than just wrappers, providing convenient methods
        #This will 'work' for anything that has some common name + '_' (like "SV_x" and "SV_y" and "SV_z")

        #Objects:
        met = Object(event, "MET")
        PV = Object(event, "PV")

        #Collections:
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        subjets = Collection(event, "SubJet")
        
        nEles = len(electrons)
        nMus = len(muons)
        nAK4Jets = len(jets)
        nAK8Jets = len(fatjets)
        nAK8SubJets = len(subjets)

        self.h_jets.Fill(nAK4Jets)
        self.h_fatjets.Fill(nAK8Jets)
        self.h_subjets.Fill(nAK8SubJets)

        nMedCSVV2 = 0
        nMedDeepB = 0

        for jet in jets:
            #Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            if jet.jetId < 2:
                continue
            # Minimum 30GeV Pt on the jets
            if jet.pt < 30:
                continue
            # Only look at jets within |eta| < 2.4
            if abs(jet.eta) > 2.4:
                continue
            # Fill 2D histo
            self.h_jet_map.Fill(jet.eta, jet.phi)

            #Count b-tagged jets with two algos at the medium working point
            #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            if jet.btagCSVV2 > 0.8838:
                nMedCSVV2 += 1
            if jet.btagDeepB > 0.4941:
                nMedDeepB += 1

        self.h_medCSVV2.Fill(nMedCSVV2)
        self.h_medDeepB.Fill(nMedDeepB)

        return True

#files=["06CC0D9B-4244-E811-8B62-485B39897212_CH01-Skim.root"]
filePrefix = "root://cms-xrd-global.cern.ch/"
files=[]
#Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
inputList =  open("../Infiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # tt + jets MC
thePostFix = "TTJets_SL"
#inputList =  open("../Infiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC
#thePostFix = "TTTT"
#inputList =  open("../Infiles/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC PSWeights
#thePostFix = "TTTT_PSWeights"
#inputList =  open("../Infiles/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # W (to Lep + Nu) + jets
#thePostFix = "WJetsToLNu"

for line in inputList:
    #.replace('\n','') protects against new line characters at end of filenames, use just str(line) if problem appears
    files.append(filePrefix + str(line).replace('\n','') )

#for file in files: 
#    print(file)

#Only take first file in extensive list:
onefile = [files[0]]
print("Opening a single file: " + str(onefile) )

p99=PostProcessor(".",
                  #files,
                  onefile,
                  cut="nJet > 3 && nFatJet > 0",
                  modules=[HistogramMaker()],
                  jsonInput=None,
                  noOut=True,
                  justcount=False,
                  postfix=thePostFix,
                  histFileName="OutHistoMaker.root",
                  histDirName="plots", 
#                  branchsel="../Infiles/kd_branchsel.txt",
#                  outputbranchsel="../Infiles/kd_branchsel.txt",
                  )

p99.run()
