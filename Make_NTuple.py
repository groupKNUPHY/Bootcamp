## Warning ##
## This code designed at a hybrid conda-environment! ##
## If you want to contact the code designer, please visit ROOM 208 and call Tau Kim ##

import uproot as ROOT
import awkward1 as ak
import vector
import numpy as np
import glob


def Eagles(filepath, filetype):
	## Get file list
	print("Start of",filetype)
	targetPattern = r""+ filepath +""
	allfiles = glob.glob(targetPattern)
	filelist = []
	for f in allfiles:
		filelist.append(f + ':Delphes')
	branches = ['Electron.PT' ,'MuonTight.PT' ,'JetPUPPI.PT','JetPUPPI.Eta','JetPUPPI.Phi','JetPUPPI.Mass','JetPUPPI.BTag',"JetPUPPIAK8.PT" ,'PuppiMissingET.MET' ,'PuppiMissingET.Phi']

	histo = {}
	count = 0
	## Fileloop
	for arrays, doc in ROOT.iterate(filelist,branches,report=True):

		print("from: {0}, to: {1} -- Entries: {2}".format(doc.start,doc.stop,len(arrays)))
		#histo = {}
		Electron = arrays[b"Electron.PT"]
		Muon = arrays[b"MuonTight.PT"]
		AK8 = arrays[b"JetPUPPIAK8.PT"]

		Jet = ak.zip(
		{
		 "PT": arrays[b"JetPUPPI.PT"],
		 "Eta": arrays[b"JetPUPPI.Eta"],
		 "Phi": arrays[b"JetPUPPI.Phi"],
		 "Mass": arrays[b"JetPUPPI.Mass"],
		 "BTag": arrays[b"JetPUPPI.BTag"]
		})

		MET = ak.zip(
		{
		 "PT": arrays[b"PuppiMissingET.MET"],
		 "Phi": arrays[b"PuppiMissingET.Phi"],
		})

		## ---------------------
		## START OF PRESELECTION
		
		## LEPTON VETO
		VETO_E = Electron[Electron > 10]
		VETO_M = Muon[Muon > 10]
		VETO_LEP = (ak.num(VETO_E) + ak.num(VETO_M)) < 1
		AK8 = AK8[VETO_LEP]
		Jet = Jet[VETO_LEP]
		MET = MET[VETO_LEP]
		
		## JET SELECT
		SELC_JET = (ak.num(Jet) >= 6) & (ak.num(AK8) >=1)
		Jet = Jet[SELC_JET]
		MET = MET[SELC_JET]

		## JET MOMENTUM
		TFIVE = Jet[Jet.PT > 25]
		SELC_25 = ak.num(TFIVE) >= 6
		Jet = Jet[SELC_25]
		MET = MET[SELC_25]

		## BTAGGING
		BTAG = Jet.BTag > 30
		BJet = Jet[BTAG]
		SELC_BTAG = ak.num(BJet) >= 2
		Jet = Jet[SELC_BTAG]
		MET = MET[SELC_BTAG]
		BJet = BJet[SELC_BTAG]

		## BJET TOPOLOGY
		deltaphi = abs(BJet.Phi[:,0] - BJet.Phi[:,1])
		deltaeta = abs(BJet.Eta[:,0] - BJet.Eta[:,1])
		
		
		## MET SR
		SELC_MET = ak.sum(MET.PT,axis=1) > 50
		Jet = Jet[SELC_MET]
		MET = MET[SELC_MET]
		BJet = BJet[SELC_MET]
		deltaphi = deltaphi[SELC_MET]
		deltaeta = deltaeta[SELC_MET]
		## END OF PRESELECTION
		## ---------------------

		## Calculate Dijet_mass
		Dijet_mass = (vector.obj(pt=Jet[:,0].PT,eta=Jet[:,0].Eta,phi=Jet[:,0].Phi,mass=Jet.Mass[:,0]) + vector.obj(pt=Jet[:,1].PT,eta=Jet[:,1].Eta,phi=Jet[:,1].Phi,mass=Jet.Mass[:,1])).mass


		## Z BOSON VETO
		VETO_Z = Dijet_mass > 110
		Jet = Jet[VETO_Z]
		MET = MET[VETO_Z]
		Djmass = Dijet_mass[VETO_Z]
		BJet = BJet[VETO_Z]
		deltaphi = deltaphi[VETO_Z]
		deltaeta = deltaeta[VETO_Z]

		## Fill NTuple
		if len(histo) == 0:

			histo['MET'] = ak.sum(MET.PT,axis=1)
			histo['HT'] = ak.sum(Jet.PT,axis=1)
			histo['Djmass'] = Djmass
			histo['deltaphi'] = deltaphi
			histo['deltaeta'] = deltaeta
		else:
			histo['MET'] = np.concatenate((histo['MET'],ak.sum(MET.PT,axis=1)))
			histo['HT'] = np.concatenate((histo['HT'],ak.sum(Jet.PT,axis=1)))
			histo['Djmass'] = np.concatenate((histo['Djmass'],Djmass))
			histo['deltaphi'] = np.concatenate((histo['deltaphi'],deltaphi))
			histo['deltaeta'] = np.concatenate((histo['deltaeta'],deltaphi))
		print(len(histo['Djmass']))

		## EOF
		#break

		## Debuging term
		#count += 1
		#if count == 10:
		#	break

	## Save Ntuple
	np.save(""+ folder +"/"+ filetype +"_nTuple",histo)
	print("End of",filetype)
	## EOF



## Main code
## QCD TARGET 1000to1500  100to200  1500to2000  2000toinf  200to300  300to500  500to700  50to100  700to1000


#### EWK BKG ####

pathlist = [
"/x4/cms/jyshin/TT_Had/condorDelPyOut/*.root",
"/x4/cms/jyshin/TT_1l/condorDelPyOut/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/TTWJets_NLO/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/TTZJets_NLO/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/WJetsToQQ/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/WJetsToLNu/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/ZJetsToQQ/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/ZJetsToNuNu/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/DYJetsLO/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/WW_NLO/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/WZ_NLO/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/ZZ_NLO/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/st_tch_NLO/*.root",
"/x4/cms/jyshin/TTBar_DM/ROOTF/st_sch_NLO/*.root",
"/CONFIDENTIAL/*.root"]


labellist = ["TT_had","TT_semi","TTW","TTZ","WQ","WL","ZQ","ZL","DY","WW","WZ","ZZ","ST_t","ST_s","???"]

#### SAVE DIRECTORY ####
folder = "Full_select_v8"


for i in range(len(pathlist)):
	Eagles(pathlist[i],labellist[i])

#print("End of Code")
