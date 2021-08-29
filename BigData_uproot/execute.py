import glob
import subprocess


##### -----Please add input hist list here
file_list  = glob.glob("RPV/Gluino1400GeV/0000/*.root")


def calc_Nout(maxfile,nfile):
	nfile = maxfile + nfile - 1
	nout = int(nfile / maxfile)
	return(nout)



##### -----Please add batch size here 
maxfile=10 # Max number of input files for each run 




nfile=len(file_list) #  Number of total input files
nout  = calc_Nout(maxfile,nfile) # Number of output files
for i in range(nout):
	start = i*maxfile 
	end = start + maxfile 
	
	infiles = (' '.join(file_list[start:end]))


	fn_out = "RPV_" + str(i) + ".npy"
	#fn_out = "QCD1000_" + str(i) + ".npy"
	#fn_out = "QCD1500_" + str(i) + ".npy"
	#fn_out = "QCD2000_" + str(i) + ".npy"


	print("############################## SET: ",fn_out)
	print(infiles)
	
	# Run specific excutable codes
	args = 'python' + ' '+ 'selector.py' + ' ' + '--outname' + ' ' + fn_out + ' '+  infiles
	subprocess.call(args,shell=True)
