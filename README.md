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

The new CMS resolved top tagger can be installed as well. For documentation see here: https://github.com/susy2015/TopTagger (this worked in July 2018, plan is to eventually port all of this into the release!

```
git clone https://github.com/susy2015/TopTagger.git TopTagger
cd TopTagger/TopTagger/test
make
# to get the make install to work on the m-machines where the paths are different than lxplus you need to make some changes to the make file. Tread carefully:
# The line: 
# PREFIX        =  /usr/local
# should be changed to:
# PREFIX        = /user/$(USER)
# which can be done with the following command (or by hand):
# cat Makefile | sed -e s%/usr/local%/user/$(USER)%g > Makefile

```

# NanoAOD Examples
```
cmsrel CMSSW_9_4_10
cd CMSSW_9_4_10/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools #official tools
git clone https://github.com/TopBrussels/NanoAODTools TopBrussels/NanoAODTools
scram b -j10
cd TopBrussels/NanoAODTools/StandaloneExamples/Book1
'''