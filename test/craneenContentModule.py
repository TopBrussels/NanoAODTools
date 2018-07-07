import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

# this producer attempts to create the same info as in https://github.com/dlont/FourTops2016/blob/master/craneens.desc
class craneenContentModuleProducer(Module) :
    def __init__(self, jetSelection):
        self.jetSel = jetSelection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        # book new branches here
        self.out.branch("NOrigJets",  "I");
        self.out.branch("1stjetpt",  "D");
        self.out.branch("2ndjetpt",  "D");
        self.out.branch("5thjetpt",  "D");
        self.out.branch("6thjetpt",  "D");
        self.out.branch("LeptonPt",  "D");
        self.out.branch("LeptonEta",  "D");
        self.out.branch("leptonIso",  "D");
        self.out.branch("leptonphi",  "D");
        self.out.branch("NjetsW",  "D");
        self.out.branch("SumJetMassX",  "D");
        self.out.branch("HT",  "D");
        self.out.branch("HT2M",  "D");
        self.out.branch("HTb",  "D");
        self.out.branch("HTH",  "D");
        self.out.branch("HTRat",  "D");
        self.out.branch("HTX",  "D");
        self.out.branch("SumJetMassX",  "D");
        self.out.branch("multitopness",  "D");
        self.out.branch("angletop1top2",  "D");
        self.out.branch("angletoplep",  "D");
        self.out.branch("LeadingBJetPt",  "D");
        self.out.branch("nLtags",  "I");
        self.out.branch("nMtags",  "I");
        self.out.branch("nTtags",  "I");
        self.out.branch("jet5and6pt",  "D");
        self.out.branch("csvJetcsv1",  "D");
        self.out.branch("csvJetcsv2",  "D");
        self.out.branch("csvJetcsv3",  "D");
        self.out.branch("csvJetcsv4",  "D");
        self.out.branch("csvJetpt1",  "D");
        self.out.branch("csvJetpt2",  "D");
        self.out.branch("csvJetpt3",  "D");
        self.out.branch("csvJetpt4",  "D");
    
        # scale factors:
        self.out.branch("ScaleFactor",  "D");
        self.out.branch("SFlepton",  "D");
        self.out.branch("SFtrig",  "D");
        self.out.branch("csvrsw[19]",  "D");
        self.out.branch("toprew",  "D");
        self.out.branch("ttxrew",  "D");
        self.out.branch("NormFactor",  "D");
        self.out.branch("weight[8]",  "D");
        self.out.branch("weight1",  "D");
        self.out.branch("weight2",  "D");
        self.out.branch("weight3",  "D");
        self.out.branch("weight4",  "D");
        self.out.branch("weight5",  "D");
        self.out.branch("weight6",  "D");
        self.out.branch("weight7",  "D");
        self.out.branch("weight8",  "D");
        self.out.branch("hdampw",  "D");
    
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        # fill new branches here
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
       
        ngoodjets=0
        HTwork=0.0
        for ijet in filter(self.jetSel,jets): #jet loop. jets are already pre-selectd by the jetSel module, effectively using the preselection criteria at the end of this program
            # jet ID should already be applied
            ngoodjets+= 1
            HTwork+=ijet.p4().Pt()
            if ngoodjets == 1:
                self.out.fillBranch("1stjetpt",ijet.p4().Pt())
            if ngoodjets == 2:
                self.out.fillBranch("2ndjetpt",ijet.p4().Pt())
            if ngoodjets == 5:
                self.out.fillBranch("5thjetpt",ijet.p4().Pt())
            if ngoodjets == 6:
                self.out.fillBranch("6thjetpt",ijet.p4().Pt())
        
        # all others need to be added still

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

#craneenContentModule = lambda : craneenContentModule(jetSelectionTight= lambda j : j.pt > 30 (j.NHF<0.90 && j.NEMF<0.90 && j.NumConst>1 && j.MUF<0.8) && ((abs(j.eta)<=2.4 && j.CHF>0 && j.CHM>0 && j.CEMF<0.90) || abs(j.eta)>2.4) && abs(j.eta)<=2.7)) # this is the tightLepVetoJetID taken from the JME wiki here https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID#Recommendations_for_13_TeV_2017 on 6 Jul 2018

craneenContentModule = lambda : craneenContentModuleProducer(jetSelection= lambda j : (j.pt > 30) )
