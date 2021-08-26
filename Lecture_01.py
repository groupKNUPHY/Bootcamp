## Lecture 01
## This code designed for HEPKNU freshmen by Taiwoo KIM.
## resisov@nate.com // resisov1124@gmail.com

import uproot as ROOT
import uproot_methods as ROOT_methods 
import numpy as np
import awkward1 as ak
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import font_manager
import mplhep as hep
import sys

## argument check
try:
	input = raw_input
except:
	pass

if len(sys.argv) < 2:
	print("Usage: macro_file_name.py input_root_file.root")

## Read your Tree
tree = ROOT.open(sys.argv[1])["LHEF"]

## We need Particle.PT, Particle.PID, Particle.Status
pt = tree["Particle.PT"].array()
pid = tree["Particle.PID"].array()
status = tree["Particle.Status"].array()


## Transverse momentum of final state electrons and muons
e_mask = ((pid == 11) & (status == 1)) | ((pid == -11) & (status == 1))
u_mask = ((pid == 13) & (status == 1)) | ((pid == -13) & (status == 1))

elec_pt = pt[e_mask].flatten()
muon_pt = pt[u_mask].flatten()

## Let's Draw histograms!
plt.hist(elec_pt,bins=30,range=(0,300),color='blue')
plt.hist(muon_pt,bins=30,range=(0,300),color='red')
plt.xlim(0,300)
plt.show()

## HOMEWORK
# Q1. 최종상태의 전자와 뮤온의 방위각 분포를 각각 히스토그램으로 그려보세요.
# hint : Particle.Phi 를 이용하세요.


# Q2. APPENDIX 를 참고해서 광자 혹은 Z 보존의 질량 분포를 히스토그램으로 그려보세요.
# hint1 : Particel.PID, Particle.M 을 활용하세요.
# hint2 : Particle.Status 는 이용하지 마세요.



## APPENDIX ##

## STANDARD MODEL PID NUMBERING SCHEME
#
#  QUARKS         ANTIQUARKS
#  d = 1	  d~ = -1
#  u = 2	  u~ = -2
#  s = 3	  s~ = -3
#  c = 4	  c~ = -4
#  b = 5	  b~ = -5
#  t = 6	  t~ = -6
#
#  LEPTONS        ANTILEPTONS
#  e-  = 11	  e+  = -11
#  ve  = 12	  ve~ = -12
#  mu- = 13	  mu+ = -13
#  vu  = 14	  vu~ = -14
#  ta- = 15	  ta+ = -15
#  vt  = 16	  vt~ = -16
#
#  BOSONS
#  g  =  21
#  a  =  22
#  z  =  23
#  w+ =  24
#  w- = -24
#
## END OF TABLE 

