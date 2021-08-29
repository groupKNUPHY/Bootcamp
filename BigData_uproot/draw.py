import mplhep as hep
import matplotlib.pyplot as plt
import numpy as np
import glob


def Stack_hist(sample_list,xsec,gen,histname):
	n_sel=0
	hsumw=0
	bins = 50
	for f in sample_list:
		
		hist_dict = np.load(f,allow_pickle=True)[()]
		hist_arr  = hist_dict[histname]
		n_sel+=  len(hist_arr)
		weight_arr = np.ones(len(hist_arr)) *Lumi * xsec / gen
		hcontents, hbin, _ = plt.hist(hist_arr,bins=bins,weights=weight_arr)
		hsumw += hcontents
	
	return hbin,hsumw,n_sel,histname

def read_data():
	RPV_path= "npys/RPV/RPV_*.npy"
	RPV_list = glob.glob(RPV_path)
	
	QCD1000_path = "npys/QCD1000/QCD1000*.npy"
	QCD1000_list = glob.glob(QCD1000_path)
	
	QCD1500_path = "npys/QCD1500/QCD1500*.npy"
	QCD1500_list = glob.glob(QCD1500_path)
	
	QCD2000_path = "npys/QCD2000/QCD2000*.npy"
	QCD2000_list = glob.glob(QCD2000_path)

	return RPV_list, QCD1000_list, QCD1500_list, QCD2000_list


if __name__ == "__main__":

	#1 --Parameter-set
	xsec_RPV	 = 0.02530
	xsec_QCD1000 =  1207
	xsec_QCD1500 =  119.9
	xsec_QCD2000 =  25.24
	
	gen_RPV = 330599
	gen_QCD1000 = 15466225
	gen_QCD1500 = 3368613
	gen_QCD2000 = 3250016
	Lumi = 63.67 * 1000
	
	#histname = 'Jet_eta'
	histname = 'Jet_phi'

	#2 --File I/O
	RPV_list, QCD1000_list, QCD1500_list, QCD2000_list = read_data()	

	#3 --Stack hist
	hbin,RPV_hsumw,RPV_sel,histname = Stack_hist(RPV_list,xsec_RPV,gen_RPV,histname)
	hbin,QCD1000_hsumw,QCD1000_sel,histname = Stack_hist(QCD1000_list,xsec_QCD1000,gen_QCD1000,histname)
	hbin,QCD1500_hsumw,QCD1500_sel,histname = Stack_hist(QCD1500_list,xsec_QCD1500,gen_QCD1500,histname)
	hbin,QCD2000_hsumw,QCD2000_sel,histname = Stack_hist(QCD2000_list,xsec_QCD2000,gen_QCD2000,histname)
	QCD_hsumw = QCD1000_hsumw + QCD1500_hsumw + QCD2000_hsumw


	print('## N Selected events')
	for i,j in zip(['RPV','QCD1000','QCD1500','QCD2000'],[RPV_sel,QCD1000_sel,QCD1500_sel,QCD2000_sel]):
		print(i,j)

	#4 --Drat hist
	plt.close()
	plt.style.use(hep.style.ROOT)
	fig, ax = plt.subplots()

	hep.histplot(RPV_hsumw, hbin,color='royalblue',histtype='step',label='RPV SUSY')
	hep.histplot(QCD_hsumw, hbin,color='crimson',histtype='step',label='QCD multi-jet')

	plt.xlabel('Leading Jet eta')
	plt.ylabel('Number of events')
	plt.ylim([1,1000000])
	plt.yscale('log')
	plt.legend()

	outname = histname + '.png'
	plt.savefig(outname)
	plt.show()
