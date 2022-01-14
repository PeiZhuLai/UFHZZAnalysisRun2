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

git cms-addpkg EgammaAnalysis/ElectronTools

git cms-addpkg RecoJets/JetProducers

git cms-addpkg PhysicsTools/PatAlgos/

git clone -b v2.3.5 https://github.com/JHUGen/JHUGenMELA

sh JHUGenMELA/MELA/setup.sh -j 8

git clone https://github.com/bachtis/Analysis.git -b KaMuCa_V4 KaMuCa

git clone -b tmp_Ferrico https://github.com/ferrico/KinZfitter.git

scramv1 b -j 8