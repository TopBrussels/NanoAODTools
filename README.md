# TopBrussels NanoAODTools

This is currently a work in progress. See also the documentation by CMS here: https://github.com/cms-nanoAOD/nanoAOD-tools

```
cmsrel CMSSW_9_4_4
cd CMSSW_9_4_4/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools #official tools
git clone https://github.com/TopBrussels/NanoAODTools TopBrussels/NanoAODTools # this code

scram b -j 10

# the important stuff is here:
cd TopBrussels/NanoAODTools/test

```
