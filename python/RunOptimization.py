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
    JOSet.setQueue("at3_8h")
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

# for 2L2b final state
list_mbb_A=["mass_bb>60","mass_bb>70","mass_bb>80"]
list_mbb_B=["mass_bb<90","mass_bb<100","mass_bb<110"]

#list_mbb_A=["mass_bb>90","mass_bb>100","mass_bb>110"]
#list_mbb_B=["mass_bb<130","mass_bb<140","mass_bb<150"]

list_mll_A=["Z_mass>70","Z_mass>75","Z_mass>80","Z_mass>85"]
list_mll_B=["Z_mass<95","Z_mass<100","Z_mass<105"]

#list_met=["met>200","met>250","met>300","met>350","met>400","met>200 && met<350","met>200 && met<300","met>200 && met<400"]
list_met=["met>200","met>250","met>300"]
list_meff=["meff_incl>500 && meff_incl<800","meff_incl>800 && meff_incl<1200","meff_incl>1200"]

list_b = ["bjets_n==2 && signal_leptons_n>=2 && pass_MET && jets_n>=2 && Z_OSLeps"] #1
list_j=["jets_n<=3","jets_n<=4","jets_n<=5","jets_n<=6","jets_n<=7","jets_n>=2"] #6
#list_dr = ["DeltaR_bb>-1", "DeltaR_bb<0.8", "DeltaR_bb<0.9", "DeltaR_bb<1.0", "DeltaR_bb<1.1", "DeltaR_bb<1.2", "DeltaR_bb<1.3", "DeltaR_bb<1.5", "DeltaR_bb<1.7", "DeltaR_bb<2.0", "DeltaR_bb<2.5"] # 11
list_met = ["met>180 && met<250","met>250 && met<400","met>400","met>450","met>180","met>250","met>300","met>350","met>500"] #9
#list_met = ["met>350","met>500"] 
list_m =["m_rho400_1>100 && m_rho400_1<140", "m_rho400_1>70 && m_rho400_1<100"] #2
list_dr = ["max(dR_rho400_1,dR_rho400_2)>-10000", "max(dR_rho400_1,dR_rho400_2)<1", "max(dR_rho400_1,dR_rho400_2)<1.25", "max(dR_rho400_1,dR_rho400_2)<1.5", "max(dR_rho400_1,dR_rho400_2)<1.75", "max(dR_rho400_1,dR_rho400_2)<2", "max(dR_rho400_1,dR_rho400_2)<2.5"] #7
"""

# for qqll final state
#list_dr = ["DeltaR_bb>-1", "DeltaR_bb<0.8", "DeltaR_bb<0.9", "DeltaR_bb<1.0", "DeltaR_bb<1.1", "DeltaR_bb<1.2", "DeltaR_bb<1.3", "DeltaR_bb<1.5", "DeltaR_bb<1.7", "DeltaR_bb<2.0", "DeltaR_bb<2.5"] # 11
#list_dr = ["DeltaR_bb>-1", "DeltaR_bb<1.0",  "DeltaR_bb<1.5", "DeltaR_bb<2.0", "DeltaR_bb<2.5"] # 5

# for 2L2b final state
#list_mbb_A=["mass_bb>60","mass_bb>70","mass_bb>80"]
#list_mbb_B=["mass_bb<90","mass_bb<100","mass_bb<110"]

#list_mbb_A=["mass_bb>90","mass_bb>100","mass_bb>110"]
#list_mbb_B=["mass_bb<130","mass_bb<140","mass_bb<150"]

#list_mll_A=["Z_mass>75","Z_mass>80","Z_mass>85"]
#list_mll_B=["Z_mass<95","Z_mass<100","Z_mass<105"]

#list_meff=["meff_incl>-1","meff_incl>300","meff_incl>500","meff_incl>600","meff_incl>700","meff_incl>800","meff_incl>900","meff_incl>1000"]



# for 4b final state

#list_dr = ["max(DeltaR_h1_dR,DeltaR_h2_dR)>1", "max(DeltaR_h1_dR,DeltaR_h2_dR)>1.25", "max(DeltaR_h1_dR,DeltaR_h2_dR)>1.5"] #3
#list_dr = ["max(DeltaR_h1_dR,DeltaR_h2_dR)>1.5"] #3
#list_dr2 = ["max(DeltaR_h1_dR,DeltaR_h2_dR)<2", "max(DeltaR_h1_dR,DeltaR_h2_dR)<2.5", "max(DeltaR_h1_dR,DeltaR_h2_dR)<3"] #3
#list_b= ["bjets_n>=3", "bjets_n>=4","bjets_n==3"] #3

#list_m1_A=["mass_h1_dR>90","mass_h1_dR>100","mass_h1_dR>110"] #3
#list_m1_B=["mass_h1_dR<130","mass_h1_dR<140","mass_h1_dR<150"] #3

#list_m1_A=["mass_h1_dR>60","mass_h1_dR>70","mass_h1_dR>80"] #3
#list_m1_B=["mass_h1_dR<90","mass_h1_dR<100","mass_h1_dR<110"] #3

#list_m2_A=["mass_h2_dR>60","mass_h2_dR>70"] #2
#list_m2_B=["mass_h2_dR<90","mass_h2_dR<100","mass_h2_dR<110"] #3
#list_m2_A=["mass_h2_dR>90","mass_h2_dR>100","mass_h2_dR>110"] #3
#list_m2_B=["mass_h2_dR<130","mass_h2_dR<140","mass_h2_dR<150"]#3


#list_m =["mass_h1_dR>70 && mass_h1_dR<110 && mass_h2_dR>60 && mass_h2_dR<90", "mass_h1_dR>110 && mass_h1_dR<150 && mass_h2_dR>60 && mass_h2_dR<90", "mass_h1_dR>110 && mass_h1_dR<150 && mass_h2_dR>90 && mass_h2_dR<140"] #3
#list_m =["mass_h1_dR>70 && mass_h1_dR<110 && mass_h2_dR>60 && mass_h2_dR<90"]
#list_m =["mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>100 && mass_h2_dR<140", "mass_h1_dR>100 && mass_h1_dR<150 && mass_h2_dR>90 && mass_h2_dR<140", "mass_h1_dR>100 && mass_h1_dR<150 && mass_h2_dR>100 && mass_h2_dR<140"] #3
#list_m=["pt_jet_4>40","pt_jet_4>25"]
#list_m =["mass_h1_dR>100 && mass_h1_dR<140 && mass_h2_dR>100 && mass_h2_dR<140"] #1
#list_met = ["met>200 && met<300","met>300 && met<450","met>450","met>400","met>200","met>250","met>300","met>350","met>500"] #9
#list_met = ["met>400","met>200","met>250","met>300","met>350"] #5
#list_m =["m_rho400_1>70 && m_rho400_1<100 && m_rho400_2>70 && m_rho400_2<100"] #1
#list_dr = ["max(DeltaR_h1_dR,DeltaR_h2_dR)>-10000", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.2", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.3", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.4", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.5", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.75","max(DeltaR_h1_dR,DeltaR_h2_dR)<2","max(DeltaR_h1_dR,DeltaR_h2_dR)<2.25","max(DeltaR_h1_dR,DeltaR_h2_dR)<2.5","max(DeltaR_h1_dR,DeltaR_h2_dR)<2.75","max(DeltaR_h1_dR,DeltaR_h2_dR)<3"] #12
#list_dr = ["max(DeltaR_h1_dR,DeltaR_h2_dR)>-10000", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1", "max(DeltaR_h1_dR,DeltaR_h2_dR)<1.25", "max(DeltaR_#h1_dR,DeltaR_h2_dR)<1.5", "max(DeltaR_h1_dR,DeltaR_h2_dR)<2", "max(DeltaR_h1_dR,DeltaR_h2_dR)<2.5", "max(DeltaR_h1_dR,DeltaR_h2_dR)<3"]

list_lep=["(baseline_electrons_n+baseline_muons_n)==0","baseline_leptons_5_n==0","baseline_leptons_10_n==0","baseline_leptons_15_n==0"]
list_jets=["jets_n>=4 && jets_n<=5","jets_n>=4 && jets_n<=6","jets_n>=4"]
list_met=["met>200","met>250","met>300","met>350","met>400"]

i=0
ii=0
for lep in list_lep:
    for jets in list_jets:
        for met in list_met:
            i+=1
            print i, lep, jets, met
            #TotalJobs += LaunchJobs([m1A, m1B, m2A, m2B, dr, meff])
                        #if i>=491 and i<591:
            TotalJobs += LaunchJobs([lep, jets, met])
print "=> Total Njobs = ", TotalJobs
##........................................................
chkFile.close()
