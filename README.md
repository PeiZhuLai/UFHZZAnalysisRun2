HZZ Analyzer for CMS Run2 UL

------

To install:

SCRAM_ARCH=slc7_amd64_gcc700; export SCRAM_ARCH

cmssw-el7

cmsrel CMSSW_10_6_26

cd CMSSW_10_6_26/src/

cmsenv

git cms-init

git clone -b UL_10_6_26 https://github.com/PeiZhuLai/UFHZZAnalysisRun2.git

git cms-addpkg DataFormats/EgammaCandidates

vi /DataFormats/EGammaCandidates/interface/photon.h
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

scram b clean

cp UFHZZAnalysisRun2/install_UL.sh .

./install_UL.sh

voms-proxy-init --rfc --voms cms

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_106X_2016ULAPV_cfg_ALP.py

==============================================================

##git cms-merge-topic asculac:Electron_XGBoost_MVA_16UL_17UL

git cms-addpkg GeneratorInterface/RivetInterface

git cms-addpkg SimDataFormats/HTXS

git cms-addpkg RecoEgamma/PhotonIdentification

git cms-addpkg RecoEgamma/ElectronIdentification

git cms-merge-topic cms-egamma:EgammaPostRecoTools

git cms-addpkg RecoEgamma/EgammaTools

git clone https://github.com/cms-egamma/EgammaPostRecoTools.git

mv EgammaPostRecoTools/python/EgammaPostRecoTools.py RecoEgamma/EgammaTools/python/.

#git clone https://github.com/cms-data/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data/

git clone -b ULSSfiles_correctScaleSysMC https://github.com/jainshilpi/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data/
(scram b clean)

git cms-addpkg EgammaAnalysis/ElectronTools

git cms-addpkg  RecoJets/JetProducers

git cms-addpkg PhysicsTools/PatAlgos/

git clone -b v2.3.5 https://github.com/JHUGen/JHUGenMELA

sh JHUGenMELA/MELA/setup.sh -j 8

git clone https://github.com/bachtis/Analysis.git -b KaMuCa_V4 KaMuCa

git clone -b tmp_Ferrico https://github.com/ferrico/KinZfitter.git

scramv1 b -j 8
(SCRAM fatal: Unable to locate the top of local release. Please run this command from a SCRAM-based area.)

voms-proxy-init --rfc --voms cms

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/Sync_106X_2018UL_cfg.py

cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/Sync_106X_2017UL_cfg.py

==============================================================

# pre-existing

#cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/Sync_102X_2017_Legacy_cfg.py

#cmsRun UFHZZAnalysisRun2/UFHZZ4LAna/python/Sync_102X_2016_Legacy_cfg.py

cp UFHZZAnalysisRun2/Utilities/crab/* .

voms-proxy-init --valid=168:00
#probably need "voms-proxy-init -voms cms -rfc"

source /cvmfs/cms.cern.ch/crab3/crab.sh

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
