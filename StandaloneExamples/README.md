# Hitchhiker's Guide to the NanoAOD
Examples created for NanoAOD using the standard PostProcessor framework.

Note about GitHub source code:
There are two collections of NanoAOD source code; one is maintained within cms-sw, and the other within cms-nanoAOD.
The latter is the collection of tools for processing NanoAOD data in a postprocessor framework, and the former contiains code for producing NanoAOD from MiniAOD.
1. <https://github.com/cms-sw/cmssw/tree/master/PhysicsTools/NanoAOD>
2. <https://github.com/cms-nanoAOD/nanoAOD-tools.git>

## Installing within CMSSW (For Python/ROOT functionality)
### DO ONCE
```bash
source $VO_CMS_SW_DIR/cmsset_default.sh	   #T2_BE MX Machines
cmsrel CMSSW_9_4_10
cd CMSSW_9_4_10/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools #The postprocessing tools!
git clone https://github.com/TopBrussels/NanoAODTools TopBrussels/NanoAODTools
scram b -j10
```


### DO EVERY NEW SESSION
```bash
cd CMSSW_9_4_10/src
cmsenv
cd TopBrussels/NanoAODTools/StandaloneExamples/
```
# Examples
## Intro Examples
```bash
cd Book1
python CH01.py
python CH02.py
python CH03.py
python CH04.py
...
```
#### CH01
This example uses a very simple configuration of the PostProcessor to instead produce a skim of data. It also demonstrates the use of a JSON in dictionary format to limit which events are accepted/written out, using TTree::Draw style preselection, and the `justcount=True` option to see how many events could pass. The skimming of data exists independently of the PostProcessor, via scripts and other tools in CMSSW, but this provides an All-In-One approach.

#### CH02
This example demonstrates creating a class that inherits from Module. This class retrieves and prints out the run, lumisection, and event number, then the number of leptons and AK4 jets. Also demonstrates the `noOut=True` option to not write the NanoAOD events passing selection.

#### CH03
Demonstrates the use of wrappers Object and Collection to group raw NanoAOD elements (for example, creating an iterable list of jets, and gaining functions for the four-momentum of a jet). Prints basic kinematic information for muons, electrons, and jets, and sums the four-momentum of them all to print out a pseudo-"event mass."

#### CH04
Demonstrates jet selection criteria, btagging, and plotting in 1D and 2D, with plots output to histogram file. Loads files from a txt list saved directly from Data Aggregation Service.

## Bigger Examples
```bash
cd StandaloneExamples/Book2
[Currently Work in Progress]
```

## Using Python Notebooks
A python notebook can be started by opening another terminal, and executing the commands:
```bash
ssh -L localhost:4444:localhost:4444 <NiceLogin>@mshort.iihe.ac.be #T2_BE
ssh -L localhost:4444:localhost:4444 <NiceLogin>@lxplus.cern.ch #LXPlus
cd path/to/CMSSW_X_Y_Z/src
cmsenv
voms-proxy-init -voms cms #Get proxy to access files over XRootD
cd path/to/notebook/directory
jupyter-notebook --no-browser --port=4444 --ip=127.0.0.1
```
When it produces a token, paste in your webbrowser to connect to homepage, and open one of the notebooks or start a new one

If there is a failure, check the Workbook to see that your Grid certificate is properly installed.

## Standdalone Notebook
Standalone.ipynb is a Standalone Jupyter Notebook that contains significant commentary and options. It dumps event information for leptons, jets, etc.