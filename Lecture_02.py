## Lecture 02
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

## Let's Draw histograms!
plt.hist(dilepton_mass,bins=150,range=(0,150),color='blue')
plt.xlim(0,150)
plt.show()


## HOMEWORK
# Q1. for 문을 사용한 이유에 대해서 생각해보세요.
# hint : 전자와 양전자의 px array(아무거나 상관없음) 를 직접 출력해보세요.


# Q2. for 문의 dilepton_mass.append((vec_nege[i,0] + vec_pose[i,0]).mass) 에서 왜 [i,0]을 사용했는지 생각해보세요.
# hint : 벡터 배열을 출력해보세요.


# Q3. 히스토그램의 분포가 무엇을 의미하는지 설명하세요.
# hint : 우리가 구한것은 dilepton의 질량입니다. 이것을 왜 구하는 걸까요?


# Q4. 로렌츠 4-벡터를 구성하는 것은 여러 방법이 있습니다. 다른 물리량들을 활용해서 벡터를 구성한 뒤,  dilepton의 mass를 다시 구해보세요.
# hint : pt, eta, phi, energy


# Q5. 전자- 전자 채널이 아닌 뮤온- 뮤온 채널에서 dilepton의 mass를 구해보세요.
# hint : PID



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

