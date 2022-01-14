import cjson
import json
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = Configuration()

config.section_('General')
config.General.workArea = 'resultsAna_JOBTAG/'
config.General.requestName = 'OUTFILENAME'
config.General.transferOutputs = True
config.General.transferLogs=True
config.General.failureLimit=1

import os
config.section_('JobType')
config.JobType.scriptExe = 'submitFileCrab.sh'
#config.JobType.inputFiles = [os.environ.get('CMSSW_BASE')+'/src/ZZMatrixElement/MEKD',os.environ.get('CMSSW_BASE')+'/src/KinZfitter/KinZfitter/ParamZ1',os.environ.get('CMSSW_BASE')+'/src/KinZfitter/HelperFunction/hists',os.environ.get('CMSSW_BASE')+'/src/ZZMatrixElement/MELA']
#config.JobType.inputFiles = [os.environ.get('CMSSW_BASE')+'/src/ZZMatrixElement/MEKD',os.environ.get('CMSSW_BASE')+'/src/KinZfitter/KinZfitter/ParamZ1',os.environ.get('CMSSW_BASE')+'/src/KinZfitter/HelperFunction/hists']
#config.JobType.inputFiles = [os.environ.get('CMSSW_BASE')+'/src/JHUGenMELA/MELA',os.environ.get('CMSSW_BASE')+'/src/KinZfitter/KinZfitter/ParamZ1',os.environ.get('CMSSW_BASE')+'/src/KinZfitter/HelperFunction/hists']
config.JobType.inputFiles = [os.environ.get('CMSSW_BASE')+'/src/KinZfitter/KinZfitter/ParamZ1',os.environ.get('CMSSW_BASE')+'/src/KinZfitter/HelperFunction/hists']
config.JobType.psetName = 'CFGFILE'
config.JobType.pluginName = 'Analysis'
config.JobType.disableAutomaticOutputCollection = True
config.JobType.outputFiles = ['OUTFILENAME.root']
config.JobType.maxMemoryMB = 2500

config.section_('Data')
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/'
config.Data.inputDataset = 'DATASETNAME'
if ('Run2018' in 'DATASETNAME'):
  #config.Data.lumiMask = 'Cert_314472-323523_13TeV_PromptReco_Collisions18_JSON.txt'##Moriond18
  #config.Data.lumiMask = 'Run2016_ReRecoJSON.txt'
  #config.Data.lumiMask = 'Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'###Legacy 18
  config.Data.lumiMask = 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
  config.Data.splitting = 'EventAwareLumiBased'
  config.Data.unitsPerJob = 100000
elif ('Run2017' in 'DATASETNAME'):
  #config.Data.lumiMask = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'###Legacy 17
  config.Data.lumiMask = 'Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
  config.Data.splitting = 'EventAwareLumiBased'
  config.Data.unitsPerJob = 100000
elif ('Run2016' in 'DATASETNAME'):
  #config.Data.lumiMask = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'###Legacy 16
  #config.Data.lumiMask = 'Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'###Legacy 16 changed
  config.Data.lumiMask = 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
  config.Data.splitting = 'EventAwareLumiBased'
  config.Data.unitsPerJob = 100000
else:
  config.Data.splitting = 'FileBased'
  if   (('GluGlu' in 'DATASETNAME') and ('MCFM701' in 'DATASETNAME') and (not 'tau' in 'DATASETNAME')): config.Data.unitsPerJob = 1
  elif (('GluGlu' in 'DATASETNAME') and ('MCFM701' in 'DATASETNAME') and ('tau' in 'DATASETNAME')): config.Data.unitsPerJob = 1
  elif (('GluGlu' in 'DATASETNAME') and (not 'MCFM701' in 'DATASETNAME')): config.Data.unitsPerJob = 1
  elif ('HToZZ' in 'DATASETNAME'): config.Data.unitsPerJob = 1
  elif ('ZZ' in 'DATASETNAME'): config.Data.unitsPerJob = 4
  elif ('TT' in 'DATASETNAME'): config.Data.unitsPerJob = 5
  else: config.Data.unitsPerJob = 5

config.Data.publication = False
#config.Data.outLFNDirBase = '/store/user/%s/2018data/UFHZZAnalysisRun2/JOBTAG/' % (getUsernameFromSiteDB())
#config.Data.outLFNDirBase = '/store/user/qguo/newNTuple_UL/UL2018/UFHZZAnalysisRun2/JOBTAG/'
config.Data.outLFNDirBase = '/store/user/zewang/JOBTAG/'
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True

config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_CN_Beijing'
#config.Site.storageSite = 'T2_US_Florida'
config.Site.whitelist = ['T2_US_*']
