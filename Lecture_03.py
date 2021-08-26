## Lecture 03
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

## We need px, py, pz, E for Lorentz 4-vector
## and also need PID and status to identify particles on the final state
px = tree["Particle.Px"].array()
py = tree["Particle.Py"].array()
pz = tree["Particle.Pz"].array()
en = tree["Particle.E"].array()
pid = tree["Particle.PID"].array()
status = tree["Particle.Status"].array()

## mask for electron and positron
nege = (pid == 11) & (status == 1)
pose = (pid == -11) & (status == 1)

## Electron px, py, pz, E
px_nege = px[nege]
py_nege = py[nege]
pz_nege = pz[nege]
en_nege = en[nege]

## Positron px, py, pz, E
px_pose = px[pose]
py_pose = py[pose]
pz_pose = pz[pose]
en_pose = en[pose]

## To make Lorentz vectors, we can use the uproot_methods module
vec_nege = ROOT_methods.TLorentzVectorArray.from_cartesian(px_nege,py_nege,pz_nege,en_nege)
vec_pose = ROOT_methods.TLorentzVectorArray.from_cartesian(px_pose,py_pose,pz_pose,en_pose)

## and then, calculation
dilepton_mass = []
for i in range(len(px)):
	if px_nege.counts[i] == 0:
		continue
	elif px_pose.counts[i] == 0:
		continue
	else:
		dilepton_mass.append((vec_nege[i,0] + vec_pose[i,0]).mass)


## now, let's make Z boson mass
mass = tree["Particle.M"].array()
zmask = (pid == 23)
z_mass = mass[zmask].flatten()

## Let's Draw histograms!
plt.hist(dilepton_mass,bins=150,range=(0,150),color='blue',histtype='step')
plt.hist(z_mass,bins=150,range=(0,150),color='red',histtype='step')
plt.xlim(0,150)
plt.show()


## HOMEWORK
# Q1. 이 분석에서 z_mass와 dilepton_mass 분포의 수 차이가 발생하는 이유는 무엇일까요?
# hint : 표준모형의 렙톤들을 잘 생각해 보세요.


# Q2. dilepton_mass의 분포에서 낮은 범위의 분포들은 왜 생기는 걸까요?
# hint : Drell Yan 프로세스를 구글에 검색해보세요.


# Q3. 전자-전자 채널과  뮤온-뮤온 채널을 병합해보세요.
# hint : 쉬움


# Q4. 병합한 결과의 사건 수와 z 보존의 숫자를 확인해보세요.
# hint : print(len(dilepton_mass))


# Q5. 이제 여러분들은 입자물리학실험에서 Z 보존을 식별하고 찾아낼 수 있습니다. 이 분석 결과를 CMS 혹은 ATLAS의 결과와 비교해보세요.



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

