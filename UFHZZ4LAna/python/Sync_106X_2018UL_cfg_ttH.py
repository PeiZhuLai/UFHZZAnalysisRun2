import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from datetime import datetime
now = datetime.now() # current date and time
#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
date = now.strftime("%d%m%Y")


process = cms.Process("UFHZZ4LAnalysis")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.MessageLogger.categories.append('UFHZZ4LAna')

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.Services_cff')
#process.GlobalTag.globaltag='106X_upgrade2018_realistic_v16'
process.GlobalTag.globaltag='106X_upgrade2018_realistic_v16_L1v1'

process.Timing = cms.Service("Timing",
                             summaryOnly = cms.untracked.bool(True)
                             )

run_events=-1
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(run_events) )

myfilelist = cms.untracked.vstring(
        #'/store/mc/RunIISummer20UL18MiniAODv2/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/30000/86509D01-06E8-5B41-82BC-C916A2857B71.root',
        #'/store/mc/RunIISummer20UL18MiniAODv2/VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/41158F86-1652-F548-B786-6F87BEB7B7E9.root',
        #'/store/mc/RunIISummer20UL18MiniAODv2/WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/EC562A9B-3860-7A4A-AFA1-9ED53D7EB60E.root',
        #'/store/mc/RunIISummer20UL18MiniAODv2/WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/270000/01072974-E38F-FD48-A5DC-B30DE99991E0.root',
        #'/store/mc/RunIISummer20UL18MiniAODv2/ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/36985B2E-3FA2-7E4B-A5FC-D20D8B713766.root',
        '/store/mc/RunIISummer20UL18MiniAODv2/ttH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/C0DA604A-0549-7844-B58B-846A0F0D9EDD.root',
)

process.source = cms.Source("PoolSource",fileNames = myfilelist,
        #eventsToProcess = cms.untracked.VEventRange('1:590706-1:590706','1:1487346-1:1487346','1:870453-1:870453','1:848227-1:848227','1:1932721-1:1932721'),
        #eventsToProcess = cms.untracked.VEventRange('1:848227-1:848227'),
                            )

process.TFileService = cms.Service("TFileService",
                                  #fileName = cms.string("Sync_1031_2018_ttH_v2.root")##
                                  fileName = cms.string("Sync_106X_2018UL_"+date+"_"+str(run_events)+"ttH_V2.root")##
)

# clean muons by segments 
process.boostedMuons = cms.EDProducer("PATMuonCleanerBySegments",
                                      src = cms.InputTag("slimmedMuons"),
                                      preselection = cms.string("track.isNonnull"),
                                      passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                                      fractionOfSharedSegments = cms.double(0.499),
                     )


# Kalman Muon Calibrations
process.calibratedMuons = cms.EDProducer("KalmanMuonCalibrationsProducer",
                                         muonsCollection = cms.InputTag("boostedMuons"),
                                         isMC = cms.bool(True),
                                         isSync = cms.bool(True),
                                         useRochester = cms.untracked.bool(True),
                                         year = cms.untracked.int32(2018)
                                         )

process.selectedElectrons = cms.EDFilter("PATElectronSelector",
                                         src = cms.InputTag("slimmedElectrons"),
                                         cut = cms.string("pt > 5 && abs(eta)<2.5")
                                         )

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    calibratedPatElectrons = cms.PSet(
        initialSeed = cms.untracked.uint32(123456), # for crab
        engineName = cms.untracked.string('TRandom3')
    )
)

####### new added
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runEnergyCorrections=False,
                       runVID=True,
                       eleIDModules=['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Summer18UL_ID_ISO_cff','RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff'],
                       phoIDModules=['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff'],
                       era='2018-UL')

process.load("RecoEgamma.EgammaTools.calibratedEgammas_cff")
process.calibratedPatElectrons.correctionFile = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2018_29Sep2020_RunFineEtaR9Gain"
process.calibratedPatElectrons.src = cms.InputTag("slimmedElectrons")

# FSR Photons
process.load('UFHZZAnalysisRun2.FSRPhotons.fsrPhotons_cff')

import os
# Jet Energy Corrections
from CondCore.DBCommon.CondDBSetup_cfi import *
#era = "Autumn18_V8_MC"
era = "Summer19UL18_V5_MC"
# for HPC
dBFile = os.environ.get('CMSSW_BASE')+"/src/UFHZZAnalysisRun2/UFHZZ4LAna/data/"+era+".db"
# for crab
#dBFile = "src/UFHZZAnalysisRun2/UFHZZ4LAna/data/"+era+".db"
process.jec = cms.ESSource("PoolDBESSource",
                          CondDBSetup,
                          connect = cms.string("sqlite_file:"+dBFile),
                          toGet =  cms.VPSet(
        cms.PSet(
            record = cms.string("JetCorrectionsRecord"),
            tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PF"),
            label= cms.untracked.string("AK4PF")
            ),
        cms.PSet(
            record = cms.string("JetCorrectionsRecord"),
            tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFchs"),
            label= cms.untracked.string("AK4PFchs")
            ),

        cms.PSet(
            record = cms.string("JetCorrectionsRecord"),
            tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK8PFchs"),
            label= cms.untracked.string("AK8PFchs")
            ),
        )
)
process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')


process.load("PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff")

process.jetCorrFactors = process.updatedPatJetCorrFactors.clone(
    src = cms.InputTag("slimmedJets"),
    levels = ['L1FastJet', 
              'L2Relative', 
              'L3Absolute'],
    payload = 'AK4PFchs' ) 

process.AK8PFJetCorrFactors = process.updatedPatJetCorrFactors.clone(
    src = cms.InputTag("slimmedJetsAK8"),
    levels = ['L1FastJet',
              'L2Relative',
              'L3Absolute'],
    payload = 'AK8PFchs' )

process.slimmedJetsJEC = process.updatedPatJets.clone(
    jetSource = cms.InputTag("slimmedJets"),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("jetCorrFactors"))
    )

process.slimmedJetsAK8JEC = process.updatedPatJets.clone(
    jetSource = cms.InputTag("slimmedJetsAK8"),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("AK8PFJetCorrFactors"))
    )

### add pileup id and discriminant to patJetsReapplyJEC
#process.load("RecoJets.JetProducers.PileupJetID_cfi")
#process.pileupJetIdUpdated = process.pileupJetId.clone(
#    jets=cms.InputTag("slimmedJets"),
#    inputIsCorrected=False,
#    applyJec=True,
#    vertexes=cms.InputTag("offlineSlimmedPrimaryVertices")
#)

from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL18
process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetIdUpdated = process.pileupJetId.clone( 
        jets=cms.InputTag("slimmedJets"),
        #inputIsCorrected=True,
        #applyJec=False,
        inputIsCorrected=False,
        applyJec=True,
        vertexes=cms.InputTag("offlineSlimmedPrimaryVertices"),
        algos = cms.VPSet(_chsalgos_106X_UL18),
    )

process.slimmedJetsJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
process.slimmedJetsJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']


# JER
process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
# for hpc
#dBJERFile = os.environ.get('CMSSW_BASE')+"/src/UFHZZAnalysisRun2/UFHZZ4LAna/data/Autumn18_V1_MC.db"
dBJERFile = os.environ.get('CMSSW_BASE')+"/src/UFHZZAnalysisRun2/UFHZZ4LAna/data/Summer19UL18_JRV2_MC.db"
## for crab
#dBFile = "src/UFHZZAnalysisRun2/UFHZZ4LAna/data/Autumn18_V1_MC.db"
process.jer = cms.ESSource("PoolDBESSource",
        CondDBSetup,
        connect = cms.string("sqlite_file:"+dBJERFile),
        toGet = cms.VPSet(
            cms.PSet(
                record = cms.string('JetResolutionRcd'),
                #tag    = cms.string('JR_Autumn18_V1_MC_PtResolution_AK4PFchs'),
                tag    = cms.string('JR_Summer19UL18_JRV2_MC_PtResolution_AK4PFchs'),
                label  = cms.untracked.string('AK4PFchs_pt')
                ),
            cms.PSet(
                record = cms.string('JetResolutionRcd'),
                #tag    = cms.string('JR_Autumn18_V1_MC_PhiResolution_AK4PFchs'),
                tag    = cms.string('JR_Summer19UL18_JRV2_MC_PhiResolution_AK4PFchs'),
                label  = cms.untracked.string('AK4PFchs_phi')
                ),
            cms.PSet(
                record = cms.string('JetResolutionScaleFactorRcd'),
                #tag    = cms.string('JR_Autumn18_V1_MC_SF_AK4PFchs'),
                tag    = cms.string('JR_Summer19UL18_JRV2_MC_SF_AK4PFchs'),
                label  = cms.untracked.string('AK4PFchs')
                )
            )
        )
process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')


#QGTag
process.load("CondCore.CondDB.CondDB_cfi")
qgDatabaseVersion = 'cmssw8020_v2'
# for hpc
QGdBFile = os.environ.get('CMSSW_BASE')+"/src/UFHZZAnalysisRun2/UFHZZ4LAna/data/QGL_"+qgDatabaseVersion+".db"
# for crab
#QGdBFile = "src/UFHZZAnalysisRun2/UFHZZ4LAna/data/QGL_"+qgDatabaseVersion+".db"
process.QGPoolDBESSource = cms.ESSource("PoolDBESSource",
      DBParameters = cms.PSet(messageLevel = cms.untracked.int32(1)),
      timetype = cms.string('runnumber'),
      toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('QGLikelihoodRcd'),
            tag    = cms.string('QGLikelihoodObject_'+qgDatabaseVersion+'_AK4PFchs'),
            label  = cms.untracked.string('QGL_AK4PFchs')
        ),
      ),
      connect = cms.string('sqlite_file:'+QGdBFile)
)
process.es_prefer_qg = cms.ESPrefer('PoolDBESSource','QGPoolDBESSource')
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets = cms.InputTag( 'slimmedJetsJEC' )
process.QGTagger.jetsLabel = cms.string('QGL_AK4PFchs')
process.QGTagger.srcVertexCollection=cms.InputTag("offlinePrimaryVertices")

# compute corrected pruned jet mass
process.corrJets = cms.EDProducer ( "CorrJetsProducer",
                                    jets    = cms.InputTag( "slimmedJetsAK8JEC" ),
                                    vertex  = cms.InputTag( "offlineSlimmedPrimaryVertices" ), 
                                    rho     = cms.InputTag( "fixedGridRhoFastjetAll"   ),
                                    payload = cms.string  ( "AK8PFchs" ),
                                    isData  = cms.bool    (  False ),
                                    year    = cms.untracked.int32(2018))


# Recompute MET
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process,
            isData=False,
            )

from PhysicsTools.PatUtils.l1PrefiringWeightProducer_cfi import l1PrefiringWeightProducer
process.prefiringweight = l1PrefiringWeightProducer.clone(
        #TheJets = cms.InputTag("updatedPatJetsUpdatedJEC"), #this should be the slimmedJets collection with up to date JECs !
        TheJets = cms.InputTag("slimmedJetsJEC"), #this should be the slimmedJets collection with up to date JECs !
        DataEraECAL = cms.string("None"),
        DataEraMuon = cms.string("20172018"),
        UseJetEMPt = cms.bool(False),
        PrefiringRateSystematicUnctyECAL = cms.double(0.2),
        PrefiringRateSystematicUnctyMuon = cms.double(0.2)
        )

# STXS
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
    inputPruned = cms.InputTag("prunedGenParticles"),
    inputPacked = cms.InputTag("packedGenParticles"),
)
process.myGenerator = cms.EDProducer("GenParticles2HepMCConverter",
    genParticles = cms.InputTag("mergedGenParticles"),
    genEventInfo = cms.InputTag("generator"),
    signalParticlePdgIds = cms.vint32(25)
)
process.rivetProducerHTXS = cms.EDProducer('HTXSRivetProducer',
  HepMCCollection = cms.InputTag('myGenerator','unsmeared'),
  LHERunInfo = cms.InputTag('externalLHEProducer'),
  ProductionMode = cms.string('AUTO'),
)
# HZZ Fiducial from RIVET
process.rivetProducerHZZFid = cms.EDProducer('HZZRivetProducer',
  HepMCCollection = cms.InputTag('myGenerator','unsmeared'),
)



# Analyzer
process.Ana = cms.EDAnalyzer('UFHZZ4LAna',
                              photonSrc    = cms.untracked.InputTag("slimmedPhotons"),
                              electronUnSSrc  = cms.untracked.InputTag("slimmedElectrons"),
                              electronSrc  = cms.untracked.InputTag("calibratedPatElectrons"),
                              muonSrc      = cms.untracked.InputTag("calibratedMuons"),
                              tauSrc      = cms.untracked.InputTag("slimmedTaus"),
                              jetSrc       = cms.untracked.InputTag("slimmedJetsJEC"),
                              mergedjetSrc = cms.untracked.InputTag("corrJets"),
                              metSrc       = cms.untracked.InputTag("slimmedMETs","","UFHZZ4LAnalysis"),
                              vertexSrc    = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
                              beamSpotSrc  = cms.untracked.InputTag("offlineBeamSpot"),
                              conversionSrc  = cms.untracked.InputTag("reducedEgamma","reducedConversions"),
                              isMC         = cms.untracked.bool(True),
                              isSignal     = cms.untracked.bool(True),
                              mH           = cms.untracked.double(125.0),
                              CrossSection = cms.untracked.double(1.0),
                              FilterEff    = cms.untracked.double(1),
                              weightEvents = cms.untracked.bool(True),
                              elRhoSrc     = cms.untracked.InputTag("fixedGridRhoFastjetAll"),
                              muRhoSrc     = cms.untracked.InputTag("fixedGridRhoFastjetAll"),
                              rhoSrcSUS    = cms.untracked.InputTag("fixedGridRhoFastjetCentralNeutral"),
                              pileupSrc     = cms.untracked.InputTag("slimmedAddPileupInfo"),
                              pfCandsSrc   = cms.untracked.InputTag("packedPFCandidates"),
                              fsrPhotonsSrc = cms.untracked.InputTag("boostedFsrPhotons"),
                              prunedgenParticlesSrc = cms.untracked.InputTag("prunedGenParticles"),
                              packedgenParticlesSrc = cms.untracked.InputTag("packedGenParticles"),
                              genJetsSrc = cms.untracked.InputTag("slimmedGenJets"),
                              generatorSrc = cms.untracked.InputTag("generator"),
                              lheInfoSrc = cms.untracked.InputTag("externalLHEProducer"),
                              reweightForPU = cms.untracked.bool(True),
                              triggerSrc = cms.InputTag("TriggerResults","","HLT"),
                              triggerObjects = cms.InputTag("selectedPatTrigger"),
                              doJER = cms.untracked.bool(True),
                              doJEC = cms.untracked.bool(True),
                              doTriggerMatching = cms.untracked.bool(False),
                              #doTriggerMatching = cms.untracked.bool(True),
                              triggerList = cms.untracked.vstring(     
                                  # Toni
                                  'HLT_Ele32_WPTight_Gsf_v', 
                                  'HLT_IsoMu24_v',
                                  'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v',
                                  'HLT_DoubleEle25_CaloIdL_MW_v',
                                  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v',
                                  'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v',
                                  'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
                                  'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
                                  'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',
                                  'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v',
                                  'HLT_TripleMu_10_5_5_DZ_v',
                                  'HLT_TripleMu_12_10_5_v',
                                  # I'm adding these
                                  'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v', 
                                  'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v', 
                              ),
                              verbose = cms.untracked.bool(False),              
                              skimLooseLeptons = cms.untracked.int32(4),              
                              skimTightLeptons = cms.untracked.int32(4),              
                              bestCandMela = cms.untracked.bool(False),   # for differential measurements
                              year = cms.untracked.int32(2018),####for year put 2016,2017, or 2018 to select correct Muon training and electron MVA
                             )

process.p = cms.Path(process.fsrPhotonSequence*
                     process.boostedMuons*
                     process.calibratedMuons*
                     process.egmGsfElectronIDSequence*
                     process.egmPhotonIDSequence*
                     process.egammaPostRecoSeq*
                     process.calibratedPatElectrons*
                     process.jetCorrFactors*
                     process.pileupJetIdUpdated*
                     process.slimmedJetsJEC*
                     process.QGTagger*
                     process.AK8PFJetCorrFactors*
                     process.slimmedJetsAK8JEC*
                     process.fullPatMetSequence*
                     process.corrJets*
                     process.mergedGenParticles*process.myGenerator*process.rivetProducerHTXS*#process.rivetProducerHZZFid*
                     process.prefiringweight*
                     process.Ana
                     )