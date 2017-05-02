import os
import string
import random
import re
import time, getpass
import socket
import sys
import datetime
#sys.path.append("../../IFAETopFramework/python/")

from BatchTools import *
from Job import *

##________________________________________________________
##
def LaunchJobs(arguments, test_file=""):
    
    Njobs = 0    
            #Setting caracteristics for the JobSet object
    JOSet = JobSet(platform)
    JOSet.setScriptDir(scriptFolder)
    JOSet.setLogDir(outputDir)
    # chiara
    if len(test_file) > 0:
        f = open(test_file, 'w')
        JOSet.setSubmissionCommandsFile(f)        
    JOSet.setTarBall(tarballPath)#tarball sent to batch (contains all executables)
    JOSet.setQueue("at3_short")
    jO = Job(platform)
        
    ## Name of the executable you want to run
    # chiara: look here!!
    jO.setExecutable("python Ottimizzazione_new.py")
    jO.setDebug(debug)
        
    name="Job_test_chiara_"+str(TotalJobs)
    jO.setName(name)            
    for arg in arguments:
        jO.addArgument(arg)
    jO.setOutDir(outputDir)                    
    JOSet.addJob(jO)

    JOSet.writeScript()
    JOSet.submitSet()
    JOSet.clear()

    Njobs += 1

    return Njobs

##________________________________________________________
## OPTIONS
debug=True
##........................................................
##________________________________________________________
## Defines some useful variables
platform = socket.gethostname()
now = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
here = os.getcwd()
##........................................................
##________________________________________________________
## Defining the paths and the tarball
outputDir="/nfs/at3/scratch2/crizzi/susy_EW/optimization_EW/Optimization_"+now+"/"
scriptFolder=here+"/Scripts_Analysis_" + now
tarballPath="/nfs/at3/scratch2/crizzi/susy_EW/optimization_EW/Optimization_tar.tgz"
prthForTarball="/nfs/at3/scratch2/crizzi/susy_EW/optimization_EW/code/"
##........................................................
##________________________________________________________
## Creating usefull repositories
os.system("mkdir -p " + scriptFolder) #script files folder
os.system("mkdir -p " + outputDir) #output files folder
##........................................................
##________________________________________________________
## Getting all samples and their associated weight/object systematics
Samples = []
#ttbar
#Samples  += [getSampleUncertainties("ttbar"          ,"410000.",[getSystematics(name="nominal",nameUp="",oneSided=True)] ,[])]
printGoodNews("--> All background samples recovered")
##........................................................
##________________________________________________________
## Defines a text file to checks all outputs are produced
chkFile = open(scriptFolder+"/JobCheck.chk","write")
##........................................................
TotalJobs = 0

prepareTarBall(prthForTarball, tarballPath)
#list_b = ["bjets_n_85>=3","bjets_n_85==3","bjets_n_85>=4", "bjets_n_77>=3","bjets_n_77==3","bjets_n_77>=4","bjets_n_70>=3","bjets_n_70==3","bjets_n_70>=4","bjets_n_60>=3","bjets_n_60==3","bjets_n_60>=4"]
#list_b = ["bjets_n>=3","bjets_n==3","bjets_n>=4"] #3

# for qqbb final state
"""
list_b = ["bjets_n==2 && signal_leptons_n==0 && dphi_min>0.4 && pass_MET && jets_n>=4"]#1
list_j=["jets_n<=5", "jets_n<=6","jets_n<=7","jets_n>=4"] #4
list_m=["mass_bb>70 && mass_bb<100 && mass_jj>70 && mass_jj<100", "mass_bb>100 && mass_bb<140 && mass_jj>70 && mass_jj<100"] #2
list_dr = ["DeltaR_bb>-1", "DeltaR_bb<0.8", "DeltaR_bb<0.9", "DeltaR_bb<1.0", "DeltaR_bb<1.1", "DeltaR_bb<1.2", "DeltaR_bb<1.3", "DeltaR_bb<1.5", "DeltaR_bb<1.7", "DeltaR_bb<2.0", "DeltaR_bb<2.5"] # 11
list_met = ["met>180 && met<250","met>250 && met<400","met>400","met>450","met>180","met>250","met>300","met>350","met>500"] #9
"""

# for 2L2b final state
list_b = ["bjets_n==2 && signal_leptons_n>=2 && pass_MET && jets_n>=2 && Z_OSLeps"] #1
list_j=["jets_n<=3","jets_n<=4","jets_n<=5","jets_n<=6","jets_n<=7","jets_n>=2"] #6
list_m=["mass_bb>70 && mass_bb<100 && Z_mass>70 && Z_mass<100", "mass_bb>100 && mass_bb<140 && Z_mass>70 && Z_mass<100"]#2
list_dr = ["DeltaR_bb>-1", "DeltaR_bb<0.8", "DeltaR_bb<0.9", "DeltaR_bb<1.0", "DeltaR_bb<1.1", "DeltaR_bb<1.2", "DeltaR_bb<1.3", "DeltaR_bb<1.5", "DeltaR_bb<1.7", "DeltaR_bb<2.0", "DeltaR_bb<2.5"] # 11
#list_met = ["met>180 && met<250","met>250 && met<400","met>400","met>450","met>180","met>250","met>300","met>350","met>500"] #9
list_met = ["met>350","met>500"] 

# for 4b final state
"""
list_dr = ["max(DeltaR_h1_dR,DeltaR_h2_dR)>-1", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.25", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.5", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.75", "max(DeltaR_h1_dR,DeltaR_h2_dR)<2", "max(DeltaR_h1_dR,DeltaR_h2_dR)<2.5", "max(DeltaR_h1_dR,DeltaR_h2_dR)<3", "max(DeltaR_h1_dR,DeltaR_h2_dR)<3.5", "max(DeltaR_h1_dR,DeltaR_h2_dR)<0.8"] #10
#list_b=["bjets_n>=3 && signal_leptons_n==0 && dphi_min>0.4 && pass_MET && jets_n>=4","bjets_n==3 && signal_leptons_n==0 && dphi_min>0.4 && pass_MET && jets_n>=4","bjets_n>=4 && signal_leptons_n==0 && dphi_min>0.4 && pass_MET && jets_n>=4"] #3
list_b=["bjets_n>=3 && signal_leptons_n==0 && dphi_min>0.4 && pass_MET && jets_n>=4","bjets_n>=4 && signal_leptons_n==0 && dphi_min>0.4 && pass_MET && jets_n>=4"] #2
list_j=["jets_n<=5","jets_n<=6","jets_n<=7","jets_n>=4"] #4
list_m =["mass_h1_dR>70 && mass_h1_dR<100 && mass_h2_dR>70 && mass_h2_dR<100", "mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>70 && mass_h2_dR<100", "mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>100 && mass_h2_dR<140"] #3
list_met = ["met>180 && met<250","met>250 && met<400","met>400","met>450","met>180","met>250","met>300","met>350","met>500"] #9
"""


#list_m=["mass_bb>70 && mass_bb<100 && mass_jj>70 && mass_jj<100", "mass_bb>100 && mass_bb<140 && mass_jj>70 && mass_jj<100"]
# ZZ
#list_m=["mass_bb>70 && mass_bb<100 && mass_jj>70 && mass_jj<100"]
# Zh


for b in list_b:
    for met in list_met:
        for m in list_m:
            for j in list_j:
                for dr in list_dr:
                    print b, met, m, j, dr
                    TotalJobs += LaunchJobs([b, met, m, j, dr])
print "=> Total Njobs = ", TotalJobs
##........................................................
chkFile.close()
