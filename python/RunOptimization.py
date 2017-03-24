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
def LaunchJobs( BtaggingOP, JetPtCut, Channel ):
    
    Njobs = 0    
        
    #Setting caracteristics for the JobSet object
    JOSet = JobSet(platform)
    JOSet.setScriptDir(scriptFolder)
    JOSet.setLogDir(outputDir)
    # chiara
    f = open('myfile.txt', 'w')
    JOSet.setSubmissionCommandsFile(f)        
    JOSet.setTarBall(tarballPath)#tarball sent to batch (contains all executables)
    JOSet.setQueue("at3_short")
    jO = Job(platform)
        
    ## Name of the executable you want to run
    # chiara: look here!!
    jO.setExecutable("python Optimization_new.py")
    jO.setDebug(debug)
        
    name="Job_test_chiara"            
    jO.setName(name)            
    OFileName = "out_chiara.root"
    jO.addOption("outputFile",OFileName) #name of the output file
    jO.setOutDir(outputDir)                    
    chkFile.write(outputDir+"/"+OFileName+"\n")        
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
outputDir="/nfs/at3/scratch2/crizzi/susy_EW/optimization/Optimization_"+now+"/"
scriptFolder=here+"/Scripts_Analysis_" + now
tarballPath="/nfs/at3/scratch2/crizzi/susy_EW/optimization/Optimization_tar.tgz"
prthForTarball="/nfs/at3/scratch2/crizzi/susy_EW/optimization/code/"
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
for BTagOP in ["85",]:
    for JetPt in ["30","40"]:
        for Channel in ["1LEPTON",]:
            print "hello"
            TotalJobs += LaunchJobs(BTagOP, JetPt, Channel)
print "=> Total Njobs = ", TotalJobs
##........................................................
chkFile.close()
