HZaTo2l2g Analyzer for CMS Run2 UL

***

# To install:

SCRAM_ARCH=slc7_amd64_gcc700; export SCRAM_ARCH

cmsrel CMSSW_10_6_26

cmssw-el7

cd CMSSW_10_6_26/src/

cmsenv

git cms-init

git clone -b UL_10_6_26 https://github.com/PeiZhuLai/UFHZZAnalysisRun2.git

git cms-addpkg DataFormats/EgammaCandidates

vi /DataFormats/EGammaCandidates/interface/photon.h

```
    /// variables added for MVA
    float e2x2()                    const {return showerShapeBlock_.e2x2;}
    float full5x5_e2x2()            const {return full5x5_showerShapeBlock_.e2x2;}
    float SCRawE()                  const {return this->superCluster()->rawEnergy();}
    float etaWidth()                const {return this->superCluster()->etaWidth();}
    float phiWidth()                const {return this->superCluster()->phiWidth();}
    float covIEtaIPhi()             const {return full5x5_showerShapeBlock_.sigmaIetaIphi;}
    float scEta()                   const {return this->superCluster()->eta();}
    float esEffSigmaRR()            const {return full5x5_showerShapeBlock_.effSigmaRR;}
    float esEnergyOverRawE()        const {return this->superCluster()->preshowerEnergy()/this->superCluster()->rawEnergy();}
```

scram b clean (scramv1 b -j 8)

cp UFHZZAnalysisRun2/install_UL.sh .

./install_UL.sh

```
voms-proxy-init --rfc --voms cms
```

### For test
```
cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/Sync_106X_2018UL_cfg_ALP.py
```
### Submit Crab

cp UFHZZAnalysisRun2/Utilities/crab/* . 

Please manual delete following codes in crabConfig_TEMPLATE.py

```
from CRABClient.UserUtilities import config, getUsernameFromCRIC

config.General.failureLimit=1
```
```
voms-proxy-init --rfc --voms cms
```
```
voms-proxy-init --valid=168:00 
```
source /cvmfs/cms.cern.ch/crab3/crab.sh

#### For Data:

```
nohup python SubmitCrabJobs.py -t "Data_2018" -d UFHZZAnalysisRun2/Sample_2018_data_UL.txt -c UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_106X_2018UL_cfg_ALP.py > SubmitCrabJobs_Data_2018.log 2>&1 &
```

#### For MC: 
```
nohup python SubmitCrabJobs.py -t "MC_2018_bkg" -d UFHZZAnalysisRun2/Sample_2018_bkg_UL.txt -c UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_106X_2018UL_cfg_ALP.py > SubmitCrabJobs_MC_2018_bkg.log 2>&1 &
```
```
nohup python SubmitCrabJobs.py -t "MC_2018_sig" -d UFHZZAnalysisRun2/Sample_2018_sig_UL.txt -c UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_106X_2018UL_cfg_ALP.py > SubmitCrabJobs_MC_2018_sig.log 2>&1 &
```
***

### Check for Crab Running Status
```
voms-proxy-init -voms cms
```
voms-proxy-init --valid=168:00

#### Check for the Status

Please use ' crab status -d resultsAna_Data_2018/crab_SingleMuon_Run2018A-UL2018_MiniAODv2-v3 ' to check how the submission process proceeds.
```
python -u manageCrabTask.py -t resultsAna_Data_2018 --report --status
```
```
python -u manageCrabTask.py -t resultsAna_MC_2018_bkg --report --status
```
```
python -u manageCrabTask.py -t resultsAna_MC_2018_sig --report --status
```
#### Kill
```
python -u manageCrabTask.py -t resultsAna_Data_2018 -k
```
```
python -u manageCrabTask.py -t resultsAna_MC_2018_bkg -k
```
```
python -u manageCrabTask.py -t resultsAna_MC_2018_sig -k
```

#### Resubmit
```
nohup python -u manageCrabTask.py -t resultsAna_Data_2018 -r -l >& managedata_Data_2018.log &
```
```
nohup python -u manageCrabTask.py -t resultsAna_MC_2018_bkg -r -l >& managedata_MC_2018_bkg.log &
```
```
nohup python -u manageCrabTask.py -t resultsAna_MC_2018_sig -r -l >& managedata_MC_2018_sig.log &
```
#### Check for nohup PIDs

ps xw

kill PID

#### Clean Crab cahe

Once all of your tasks are done, you should run the following command to purge your crab cache so that it doesn't fill up:

python manageCrabTask.py -t resultsAna_Data_2018 -p

python manageCrabTask.py -t resultsAna_MC_2018_bkg -p

python manageCrabTask.py -t resultsAna_MC_2018_sig -p

#### See your Crab Output file

Notice: re-login your account without CMSSW environment (Need not cmsenv)

```
voms-proxy-init -voms cms
```

```
gfal-ls -l https://cceos.ihep.ac.cn:9000/eos/ihep/cms/store/user/pelai
```

#### See your Crab Output file
```
gfal-rm -r https://cceos.ihep.ac.cn:9000/eos/ihep/cms/store/user/pelai/<file_or_dir_to_delete>
```

#### For crab

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_106X_2016UL_cfg_ALP.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_106X_2016ULAPV_cfg_ALP.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_106X_2017UL_cfg_ALP.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_106X_2018UL_cfg_ALP.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_106X_2016UL_cfg_ALP.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_106X_2016ULAPV_cfg_ALP.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_106X_2017UL_cfg_ALP.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_106X_2018UL_cfg_ALP.py

***

# pre-existing

#cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/Sync_102X_2017_Legacy_cfg.py

#cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/Sync_102X_2016_Legacy_cfg.py

cp UFHZZAnalysisRun2/Utilities/crab/* .

voms-proxy-init --valid=168:00
#probably need "voms-proxy-init -voms cms -rfc"

source /cvmfs/cms.cern.ch/crab3/crab.sh

For Data:

python SubmitCrabJobs.py -t "myTask_Data" -d datasets_2016ReReco.txt -c UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_80X_M1703Feb_2l_cfg.py

or similary for MC:

python SubmitCrabJobs.py -t "myTask_MC" -d datasets_Summer16_25ns_MiniAOD.txt -c UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_80X_M17_4l_cfg.py

You can use manageCrabTask.py to check the status, resubmit, or kill your task. E.g. after submitting:

nohup python -u manageCrabTask.py -t resultsAna_Data_M17_Feb19 -r -l >& managedata.log &

This will start an infinite loop of running crab resubmit on all of your tasks, then sleep for 30min. You should kill the process once all of your tasks are done. Once all of your tasks are done, you should run the following command to purge your crab cache so that it doesn't fill up:

python manageCrabTask.py -t resultsAna_Data_M17_Feb19 -p

UFHZZ4LAna/python/templateMC_102X_Legacy16_4l_cfg.py
UFHZZ4LAna/python/templateMC_102X_Legacy17_4l_cfg.py
UFHZZ4LAna/python/templateMC_102X_Legacy18_4l_cfg.py
UFHZZ4LAna/python/templateData_102X_Legacy16_3l_cfg.py
UFHZZ4LAna/python/templateData_102X_Legacy17_3l_cfg.py
UFHZZ4LAna/python/templateData_102X_Legacy18_3l_cfg.py
